import truststore
truststore.inject_into_ssl()

import os
import gradio as gr
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

# from llama_index.llms.openai import OpenAI
load_dotenv()

# 1. הגדרת המודלים (חשוב להשתמש באותו Embedding שהשתמשנו ב-ingest)
embed_model = CohereEmbedding(
    api_key=os.environ["COHERE_API_KEY"],
    model_name="embed-multilingual-v3.0",
)
# נשתמש ב-OpenAI כדי "לנסח" את התשובה הסופית
# במקום OpenAI
llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

# 2. טעינת האינדקס מהתיקייה המקומית
print("Loading knowledge base from storage...")
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)

# 3. יצירת מנוע השאילתות (Query Engine)
query_engine = index.as_query_engine(llm=llm)

# 4. פונקציה שמקבלת שאלה ומחזירה תשובה
def ask_bot(question):
    response = query_engine.query(question)
    return str(response)

# 5. יצירת הממשק הגרפי עם Gradio
# הגדרת הממשק הגרפי עם שדה פלט מוגדל
demo = gr.Interface(
    fn=ask_bot,
    inputs=gr.Textbox(lines=2, placeholder="שאלי משהו על קבצי ה-MD שלך..."),
    # כאן אנחנו מגדירים את ה-Output בצורה מפורטת
    outputs=gr.Textbox(
        label="תשובת המערכת", 
        lines=15,          # מספר השורות שיוצגו כברירת מחדל (זה מגדיל את הגובה)
        max_lines=30,      # המקסימום שהשדה יתרחב אליו לפני שתופיע גלילה
        show_copy_button=True # בונוס: כפתור להעתקה מהירה של התשובה
    ),
    title="RAG System (Cohere Powered)",
    description="מערכת השאלות והתשובות שלך על בסיס תיעוד ה-AI"
)

if __name__ == "__main__":
    print("Starting Gradio server...")
    demo.launch()
