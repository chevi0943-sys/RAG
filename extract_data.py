# import os
# import json
# import asyncio
# from pydantic import BaseModel, Field
# from typing import List
# from llama_index.core import SimpleDirectoryReader
# from llama_index.llms.cohere import Cohere
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # חלק א': הגדרת הסכמות (Schemas) עם Pydantic
# # ==========================================
# from pydantic import BaseModel, Field
# from typing import List

# class Decision(BaseModel):
#     """מייצג החלטה טכנית או ארכיטקטונית שהתקבלה בפרויקט"""
#     id: str = Field(description="מזהה ייחודי קצר באנגלית, למשל dec-001")
#     title: str = Field(description="כותרת קצרה ועניינית של ההחלטה")
#     summary: str = Field(description="תקציר ההחלטה והסיבה המרכזית בגללה היא התקבלה")
#     tags: List[str] = Field(description="רשימה של 2-3 תגיות רלוונטיות, למשל ['db', 'frontend']")

# class Rule(BaseModel):
#     """מייצג כלל או הנחיית פיתוח שיש לעמוד בהם"""
#     id: str = Field(description="מזהה ייחודי באנגלית, למשל rule-001")
#     rule_description: str = Field(description="תיאור הכלל, למשל 'כל מסך בעברית חייב להיות מיושר לימין RTL'")
#     scope: str = Field(description="התחום עליו חל הכלל (למשל: ui, backend, auth)")

# class WarningItem(BaseModel):
#     """מייצג אזהרה, מגבלה טכנית או אזור רגיש בקוד"""
#     id: str = Field(description="מזהה ייחודי באנגלית, למשל warn-001")
#     message: str = Field(description="תוכן האזהרה או המגבלה")
#     severity: str = Field(description="רמת החומרה: high, medium, low")

# class ExtractedKnowledge(BaseModel):
#     """אוסף כל ההחלטות, הכללים והאזהרות שחולצו ממסמך תיעוד"""
#     decisions: List[Decision] = Field(default_factory=list, description="רשימת ההחלטות שנמצאו במסמך")
#     rules: List[Rule] = Field(default_factory=list, description="רשימת הכללים וההנחיות שנמצאו במסמך")
#     warnings: List[WarningItem] = Field(default_factory=list, description="רשימת אזהרות או אזורים רגישים במסמך")


# # ==========================================
# # חלק ב': פונקציית החילוץ והשמירה
# # ==========================================

# async def extract_data_from_md_files():
#     # 1. אתחול המודל (חובה להשתמש במודל שתומך ב-Structured Outputs, ו-Command-R מצוין לזה)
#     llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

#     # 2. טעינת קבצי ה-md שלך מתיקיית התיעוד (שני את הנתיב לתיקייה האמיתית שלך)
#     print("Loading Markdown files...")
#     documents = SimpleDirectoryReader("./my_project", required_exts=[".md"], recursive=True).load_data()

#     # נייצר אובייקט אחד ריק שיצבור את כל המידע מכל הקבצים
#     all_knowledge = ExtractedKnowledge()

#     # 3. מעבר על כל מסמך וחילוץ המידע
#     for doc in documents:
#         file_name = doc.metadata.get('file_name', 'unknown')
#         print(f"Extracting structured data from: {file_name}...")
        
#         # זה הפרומפט שיישלח יחד עם הדרישה לעמוד בסכמה
#         prompt_template = (
#             f"קרא את מסמך התיעוד הבא מתוך כלי Agentic Coding.\n"
#             f"חלץ מתוכו את כל ההחלטות (Decisions) והכללים (Rules) שאתה מזהה.\n"
#             f"אם אין כאלה, החזר רשימות ריקות.\n\n"
#             f"טקסט המסמך:\n{doc.text}"
#         )
        
#         try:
#             # הפעלת הקסם של LlamaIndex: הוא דואג שהפלט יחזור כאובייקט ExtractedKnowledge!
#             result = await llm.astructured_predict(
#                 ExtractedKnowledge, 
#                 prompt_template=prompt_template
#             )
            
#             # הוספת התוצאות לאוסף הכללי שלנו
#             all_knowledge.decisions.extend(result.decisions)
#             all_knowledge.rules.extend(result.rules)
            
#         except Exception as e:
#             print(f"Error extracting from {file_name}: {e}")

#     # 4. שמירת התוצאות לקובץ JSON
#     output_file = "structured_data.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         # הפקודה model_dump() ממירה את אובייקט ה-Pydantic למילון רגיל של פייתון
#         json.dump(all_knowledge.model_dump(), f, ensure_ascii=False, indent=2)
        
#     print(f"\n✅ סיום בהצלחה! הנתונים נשמרו לקובץ {output_file}")
#     print(f"חולצו סך הכל {len(all_knowledge.decisions)} החלטות ו-{len(all_knowledge.rules)} כללים.")

# if __name__ == "__main__":
#     asyncio.run(extract_data_from_md_files())




# import os
# import json
# import asyncio
# from pydantic import BaseModel, Field
# from typing import List
# from llama_index.core import SimpleDirectoryReader
# from llama_index.llms.cohere import Cohere
# from llama_index.core import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # חלק א': הגדרת הסכמות (Descriptions באנגלית לשיפור הביצועים)
# # ==========================================
# class Decision(BaseModel):
#     id: str = Field(description="Unique ID, e.g., dec-001")
#     title: str = Field(description="Short title of the technical decision")
#     summary: str = Field(description="The full context and reason for the decision")
#     tags: List[str] = Field(description="2-3 relevant tags, e.g., ['database', 'frontend']")

# class Rule(BaseModel):
#     id: str = Field(description="Unique ID, e.g., rule-001")
#     rule_description: str = Field(description="The actual rule or guideline the developer must follow")
#     scope: str = Field(description="The scope of the rule, e.g., ui, backend, auth")

# class WarningItem(BaseModel):
#     id: str = Field(description="Unique ID, e.g., warn-001")
#     message: str = Field(description="The warning message, technical limitation, or sensitive area")
#     severity: str = Field(description="Severity level: high, medium, or low")

# class ExtractedKnowledge(BaseModel):
#     decisions: List[Decision] = Field(default_factory=list, description="List of technical decisions")
#     rules: List[Rule] = Field(default_factory=list, description="List of rules and guidelines")
#     warnings: List[WarningItem] = Field(default_factory=list, description="List of warnings and limitations")


# # ==========================================
# # חלק ב': פונקציית החילוץ והשמירה
# # ==========================================

# async def extract_data_from_md_files():
#     llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

#     print("🔍 מחפש קבצים בתיקייה: ./my_project")
#     documents = SimpleDirectoryReader("./my_project", required_exts=[".md"], recursive=True).load_data()
#     print(f"✅ מצאתי {len(documents)} קבצים!")

#     all_knowledge = ExtractedKnowledge()

#     for doc in documents:
#         file_name = doc.metadata.get('file_name', 'unknown')
#         print(f"\n📄 מחלץ נתונים מתוך: {file_name}...")
        
#         prompt_template = (
#             "You are an expert technical data extractor.\n"
#             "Read the following technical documentation and extract all:\n"
#             "1. Decisions (החלטות טכניות)\n"
#             "2. Rules (חוקי פיתוח, הנחיות)\n"
#             "3. Warnings (אזהרות, מגבלות, אזורים רגישים)\n\n"
#             "Keep the extracted text in Hebrew exactly as it appears in the text.\n"
#             "If none exist for a category, leave it empty.\n\n"
#             "Document Text:\n"
#             "---------------------\n"
#             f"{doc.text}\n"
#             "---------------------\n"
#         )
        
#         try:
#             # הופכים את הטקסט שלנו לאובייקט PromptTemplate רשמי
#             prompt_obj = PromptTemplate(prompt_template)
            
#             # מעבירים את זה לפרמטר 'prompt'
#             result = await llm.astructured_predict(
#                 ExtractedKnowledge, 
#                 prompt=prompt_obj
#             )
            
#             all_knowledge.decisions.extend(result.decisions)
#             all_knowledge.rules.extend(result.rules)
#             all_knowledge.warnings.extend(result.warnings)
            
#             print(f"   ✅ חולצו: {len(result.decisions)} החלטות, {len(result.rules)} חוקים, {len(result.warnings)} אזהרות.")
            
#         except Exception as e:
#             print(f"   ❌ שגיאה בחילוץ מהקובץ: {e}")

#     output_file = "structured_data.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(all_knowledge.model_dump(), f, ensure_ascii=False, indent=2)
        
#     print(f"\n🎉 סיום בהצלחה! הנתונים נשמרו לקובץ {output_file}")

# if __name__ == "__main__":
#     asyncio.run(extract_data_from_md_files())














# import os
# import json
# import asyncio
# from pydantic import BaseModel, Field
# from typing import List
# from llama_index.core import SimpleDirectoryReader, PromptTemplate
# from llama_index.core.output_parsers import PydanticOutputParser
# from llama_index.llms.cohere import Cohere
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # חלק א': הגדרת הסכמות (Schemas)
# # ==========================================
# class Decision(BaseModel):
#     id: str = Field(description="Unique ID, e.g., dec-001")
#     title: str = Field(description="Short title of the technical decision")
#     summary: str = Field(description="The full context and reason for the decision")
#     tags: List[str] = Field(description="2-3 relevant tags, e.g., ['database', 'frontend']")

# class Rule(BaseModel):
#     id: str = Field(description="Unique ID, e.g., rule-001")
#     rule_description: str = Field(description="The actual rule or guideline the developer must follow")
#     scope: str = Field(description="The scope of the rule, e.g., ui, backend, auth")

# class WarningItem(BaseModel):
#     id: str = Field(description="Unique ID, e.g., warn-001")
#     message: str = Field(description="The warning message, technical limitation, or sensitive area")
#     severity: str = Field(description="Severity level: high, medium, or low")

# class ExtractedKnowledge(BaseModel):
#     decisions: List[Decision] = Field(default_factory=list, description="List of technical decisions")
#     rules: List[Rule] = Field(default_factory=list, description="List of rules and guidelines")
#     warnings: List[WarningItem] = Field(default_factory=list, description="List of warnings and limitations")

# # ==========================================
# # חלק ב': פונקציית החילוץ (המעודכנת לפארסר יציב)
# # ==========================================
# async def extract_data_from_md_files():
#     llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

#     print("🔍 מחפש קבצים בתיקייה: ./my_project")
#     documents = SimpleDirectoryReader("./my_project", required_exts=[".md"], recursive=True).load_data()
#     print(f"✅ מצאתי {len(documents)} קבצים!")

#     all_knowledge = ExtractedKnowledge()

#     # שימוש בפארסר חזק יותר שלא מסתמך על Tool Calling בלבד
#     parser = PydanticOutputParser(ExtractedKnowledge)
#     format_instructions = parser.get_format_string()

#     for doc in documents:
#         file_name = doc.metadata.get('file_name', 'unknown')
#         print(f"\n📄 מחלץ נתונים מתוך: {file_name}...")
        
#         prompt_template = (
#             "You are an expert technical data extractor.\n"
#             "Read the following technical documentation and extract all:\n"
#             "1. Decisions (החלטות טכניות)\n"
#             "2. Rules (חוקי פיתוח, הנחיות)\n"
#             "3. Warnings (אזהרות, מגבלות, אזורים רגישים)\n\n"
#             "Keep the extracted text in Hebrew exactly as it appears in the text.\n"
#             "If none exist for a category, leave it empty.\n\n"
#             "MUST output ONLY valid JSON according to the following schema:\n"
#             "{format_instructions}\n\n"
#             "Document Text:\n"
#             "---------------------\n"
#             "{text}\n"
#             "---------------------\n"
#         )
        
#         prompt_obj = PromptTemplate(template=prompt_template)
        
#         try:
#             # שימוש ב-apredict רגיל שולח את הבקשה ומקבל טקסט JSON חזרה
#             response = await llm.apredict(
#                 prompt_obj, 
#                 format_instructions=format_instructions,
#                 text=doc.text
#             )
            
#             # המרת טקסט ה-JSON לאובייקט Pydantic שלנו
#             result = parser.parse(response)
            
#             all_knowledge.decisions.extend(result.decisions)
#             all_knowledge.rules.extend(result.rules)
#             all_knowledge.warnings.extend(result.warnings)
            
#             print(f"   ✅ חולצו: {len(result.decisions)} החלטות, {len(result.rules)} חוקים, {len(result.warnings)} אזהרות.")
            
#         except Exception as e:
#             print(f"   ❌ שגיאה בחילוץ מהקובץ: {e}")

#     output_file = "structured_data.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(all_knowledge.model_dump(), f, ensure_ascii=False, indent=2)
        
#     print(f"\n🎉 סיום בהצלחה! הנתונים נשמרו לקובץ {output_file}")

# if __name__ == "__main__":
#     asyncio.run(extract_data_from_md_files())
























# import os
# import json
# import asyncio
# import urllib3
# import truststore
# from pydantic import BaseModel, Field
# from typing import List
# from llama_index.core import SimpleDirectoryReader, PromptTemplate
# from llama_index.core.output_parsers import PydanticOutputParser
# from llama_index.llms.cohere import Cohere
# from dotenv import load_dotenv












# # הזרקת אבטחה - קריטי כדי שהקריאות לרשת לא יתקעו!
# truststore.inject_into_ssl()
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# load_dotenv()

















import os
import json
import asyncio
import urllib3
import truststore
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 1. הזרקת אבטחה וביטול אזהרות (בדיוק כמו ב-Workflow שלך)
truststore.inject_into_ssl()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# ייבוא רכיבי LlamaIndex הדרושים לחילוץ
from llama_index.core import SimpleDirectoryReader, PromptTemplate
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.llms.cohere import Cohere






# ==========================================
# חלק א': הגדרת הסכמות (Schemas)
# ==========================================
class Decision(BaseModel):
    id: str = Field(description="Unique ID, e.g., dec-001")
    title: str = Field(description="Short title of the technical decision")
    summary: str = Field(description="The full context and reason for the decision")
    tags: List[str] = Field(description="2-3 relevant tags, e.g., ['database', 'frontend']")

class Rule(BaseModel):
    id: str = Field(description="Unique ID, e.g., rule-001")
    rule_description: str = Field(description="The actual rule or guideline the developer must follow")
    scope: str = Field(description="The scope of the rule, e.g., ui, backend, auth")

class WarningItem(BaseModel):
    id: str = Field(description="Unique ID, e.g., warn-001")
    message: str = Field(description="The warning message, technical limitation, or sensitive area")
    severity: str = Field(description="Severity level: high, medium, or low")

class ExtractedKnowledge(BaseModel):
    decisions: List[Decision] = Field(default_factory=list, description="List of technical decisions")
    rules: List[Rule] = Field(default_factory=list, description="List of rules and guidelines")
    warnings: List[WarningItem] = Field(default_factory=list, description="List of warnings and limitations")

# ==========================================
# חלק ב': פונקציית החילוץ
# ==========================================
async def extract_data_from_md_files():
    llm = Cohere(api_key=os.environ["COHERE_API_KEY"], model="command-r-08-2024")

    print("🔍 מחפש קבצים בתיקייה: ./my_project")
    documents = SimpleDirectoryReader("./my_project", required_exts=[".md"], recursive=True).load_data()
    print(f"✅ מצאתי {len(documents)} קבצים!")

    all_knowledge = ExtractedKnowledge()
    parser = PydanticOutputParser(ExtractedKnowledge)
    format_instructions = parser.get_format_string()

    for doc in documents:
        file_name = doc.metadata.get('file_name', 'unknown')
        print(f"\n📄 מחלץ נתונים מתוך: {file_name}...")
        
        prompt_template = (
            "You are an expert technical data extractor.\n"
            "Read the following technical documentation and extract all:\n"
            "1. Decisions (החלטות טכניות)\n"
            "2. Rules (חוקי פיתוח, הנחיות)\n"
            "3. Warnings (אזהרות, מגבלות, אזורים רגישים)\n\n"
            "Keep the extracted text in Hebrew exactly as it appears in the text.\n"
            "If none exist for a category, leave it empty.\n\n"
            "MUST output ONLY valid JSON according to the following schema:\n"
            "{format_instructions}\n\n"
            "Document Text:\n"
            "---------------------\n"
            "{text}\n"
            "---------------------\n"
        )
        
        prompt_obj = PromptTemplate(template=prompt_template)
        
        try:
            response = await llm.apredict(
                prompt_obj, 
                format_instructions=format_instructions,
                text=doc.text
            )
            
            try:
                # מנסים לפרסס את התשובה
                result = parser.parse(response)
                all_knowledge.decisions.extend(result.decisions)
                all_knowledge.rules.extend(result.rules)
                all_knowledge.warnings.extend(result.warnings)
                print(f"   ✅ חולצו: {len(result.decisions)} החלטות, {len(result.rules)} חוקים, {len(result.warnings)} אזהרות.")
            except Exception as parse_error:
                print(f"   ❌ שגיאה בפענוח ה-JSON מהמודל: {parse_error}")
                print(f"   [תוכן גולמי שהתקבל]:\n{response}\n")
            
        except Exception as e:
            print(f"   ❌ שגיאת רשת/API: {e}")

    output_file = "structured_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_knowledge.model_dump(), f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 סיום בהצלחה! הנתונים נשמרו לקובץ {output_file}")

if __name__ == "__main__":
    asyncio.run(extract_data_from_md_files())