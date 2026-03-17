

import os
import json
import asyncio
import urllib3
import truststore
from typing import List
from dotenv import load_dotenv

# הזרקת אבטחה וביטול אזהרות
truststore.inject_into_ssl()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

from llama_index.core.workflow import (
    Workflow, 
    StartEvent, 
    StopEvent, 
    Event, 
    Context, 
    step as llama_step
)
from llama_index.core.base.llms.types import ChatMessage 
from llama_index.core.schema import NodeWithScore
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.utils.workflow import draw_all_possible_flows
import gradio as gr

# 1. הגדרת האירועים (הוספנו את אירועי הניתוב)
class SemanticSearchEvent(Event):
    query: str

class StructuredSearchEvent(Event):
    query: str

class RetrieverEvent(Event):
    nodes: List[NodeWithScore]
    query: str

class ValidationEvent(Event):
    nodes: List[NodeWithScore]
    query: str

class RewriteEvent(Event):
    query: str

# 2. מחלקת ה-Workflow
class RAGWorkflow(Workflow):
    def __init__(self, llm, retriever, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm
        self.retriever = retriever

    @llama_step
    async def route_query(self, ev: StartEvent) -> SemanticSearchEvent | StructuredSearchEvent:
        print(f"--- Router: מנתח את השאלה: '{ev.query}' ---")
        
        prompt = (
            f"עליך לנתח את שאלת המשתמש: '{ev.query}'\n"
            "ענה 'מובנה' אם השאלה מבקשת רשימה, ספירה (כמה יש), או נתונים טכניים ספציפיים (החלטות, חוקים, אזהרות).\n"
            "ענה 'סמנטי' אם השאלה מבקשת הסבר, תיאור כללי, או איך דברים עובדים.\n"
            "ענה בדיוק מילה אחת: 'מובנה' או 'סמנטי'."
        )
        
        message = ChatMessage(role="user", content=prompt)
        response = await self.llm.achat([message])
        decision = response.message.content.strip()
        
        if "מובנה" in decision:
            print("-> ניתוב: מובנה (JSON)")
            return StructuredSearchEvent(query=ev.query)
        else:
            print("-> ניתוב: סמנטי (Vector Index)")
            return SemanticSearchEvent(query=ev.query)

    @llama_step
    async def retrieve_structured(self, ev: StructuredSearchEvent) -> StopEvent:
        print("Running step retrieve_structured...")
        try:
            with open("structured_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return StopEvent(result="שגיאה: קובץ structured_data.json לא נמצא.")

        prompt = (
            f"בהתבסס על הנתונים המובנים הבאים:\n{json.dumps(data, ensure_ascii=False)}\n"
            f"ענה על השאלה: {ev.query}"
        )
        message = ChatMessage(role="user", content=prompt)
        response = await self.llm.achat([message])
        return StopEvent(result=str(response.message.content))

    @llama_step
    async def retrieve(self, ev: SemanticSearchEvent) -> ValidationEvent:
        print(f"Running step retrieve (Semantic) for: {ev.query}")
        nodes = self.retriever.retrieve(ev.query)
        return ValidationEvent(nodes=nodes, query=ev.query)

    @llama_step
    async def validate(self, ev: ValidationEvent) -> RetrieverEvent | RewriteEvent:
        print("Running step validate...")
        if not ev.nodes:
            return RewriteEvent(query=ev.query)

        context = "\n".join([n.text for n in ev.nodes])
        prompt = f"האם המידע הבא עוזר לענות על השאלה: '{ev.query}'?\nמידע:\n{context}\nענה רק 'כן' או 'לא'."
        
        message = ChatMessage(role="user", content=prompt)
        response = await self.llm.achat([message])
        if "כן" in response.message.content:
            return RetrieverEvent(nodes=ev.nodes, query=ev.query)
        return RewriteEvent(query=ev.query)

    @llama_step
    async def synthesize(self, ev: RetrieverEvent) -> StopEvent:
        print("Running step synthesize...")
        context = "\n".join([n.text for n in ev.nodes])
        prompt = f"בהתבסס על המידע:\n{context}\n ענה על:ענה בצורה קצרה וממוקדת. אם המידע לא קיים, ציין זאת בפשטות  {ev.query}"
        response = await self.llm.achat([ChatMessage(role="user", content=prompt)])
        return StopEvent(result=str(response.message.content))

    @llama_step
    async def rewrite_query(self, ctx: Context, ev: RewriteEvent) -> StartEvent | StopEvent:
        if not hasattr(self, "_retries"): self._retries = 0
        if self._retries >= 2: 
            self._retries = 0
            return StopEvent(result="לא מצאתי מידע רלוונטי בתיעוד.")
        
        self._retries += 1
        print(f"--- Retry {self._retries} ---")
        prompt = f"השאילתה '{ev.query}' לא מצאה תוצאות. נסח שאילתה טכנית טובה יותר לחיפוש בתיעוד."
        response = await self.llm.achat([ChatMessage(role="user", content=prompt)])
        return StartEvent(query=response.message.content.strip())

# 3. ממשק Gradio והרצה
async def chat_interface(message, history):
    w = RAGWorkflow(llm=llm, retriever=retriever, timeout=60)
    result = await w.run(query=message)
    return str(result)



# ==========================================
# אתחול המערכת (מחוץ לפונקציות כדי ש-Reload יעבוד)
# ==========================================

print("Initializing models and index...")
llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")
embed_model = CohereEmbedding(api_key=os.environ["COHERE_API_KEY"], model_name="embed-multilingual-v3.0")

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)
retriever = index.as_retriever(similarity_top_k=3)

# יצירת ה-Workflow ושמירת התרשים
# w = RAGWorkflow(llm=llm, retriever=retriever, timeout=60)
# draw_all_possible_flows(w, filename="workflow_graph.html")

# ==========================================
# יצירת הממשק (המשתנה demo עכשיו גלובלי)
# ==========================================

with gr.Blocks(css="style.css", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("<h1 style='text-align: center; color: #2c3e50;'>🤖 Agentic RAG Assistant</h1>")
    
    with gr.Column(elem_id="instructions-box"):
        gr.HTML("""
            <div dir="rtl" style="max-width: 800px; margin: 0 auto;">
                <h3 style="color: #4a90e2; margin-bottom: 5px;">📝 מה אפשר לשאול אותי?</h3>
                <p style="margin-top: 0; font-size: 1.1em;">
                אני כאן כדי לעזור לך לנווט בתיעוד הפרויקט. את יכולה לשאול אותי על <b>החלטות טכניות שהתקבלו</b>, <b>חוקי פיתוח ו-UI</b>, <b>אזהרות</b>, או פשוט לבקש הסברים כלליים על הקוד והארכיטקטורה.
                </p>
            </div>
        """)

    gr.ChatInterface(
        fn=chat_interface,
        examples=["אילו החלטות התקבלו?", "מהם חוקי ה-UI?", "באיזו שפה הפרויקט כתוב?"],
        cache_examples=False,
    )

# ההפעלה הרגילה (במידה ולא משתמשים ב-reload)
if __name__ == "__main__":
    demo.launch()