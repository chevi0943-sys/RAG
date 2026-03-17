# # 1. קודם כל - הזרקת ה-SSL דרך truststore (הכי חשוב!)
# import truststore
# truststore.inject_into_ssl()

# import os
# import ssl
# import urllib3

# # 2. גיבוי: ביטול אימות SSL גלובלי
# ssl._create_default_https_context = ssl._create_unverified_context
# os.environ['CURL_CA_BUNDLE'] = ""
# os.environ['PYTHONHTTPSVERIFY'] = "0"
# # פקודה קריטית עבור הספריות החדשות של Pinecone/OpenAI
# os.environ['SSL_CERT_FILE'] = "" 

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # 3. עכשיו ה-Imports הרגילים
# from dotenv import load_dotenv
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from llama_index.embeddings.cohere import CohereEmbedding
# from pinecone import Pinecone

# load_dotenv()

# # המשך הפונקציה start_ingestion כפי שכתבת...

# def start_ingestion():
#     # שימוש ב-Cohere שכבר מותקן
#     embed_model = CohereEmbedding(
#         api_key=os.environ["COHERE_API_KEY"],
#         model_name="embed-multilingual-v3.0",
#     )

#     pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
#     pinecone_index = pc.Index("first-pinecone")
    
#     vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     print("Loading documents...")
#     documents = SimpleDirectoryReader("./my_project", recursive=True).load_data()

#     print("Indexing and uploading... (זה אמור לעבוד עכשיו)")
#     index = VectorStoreIndex.from_documents(
#         documents, 
#         storage_context=storage_context,
#         embed_model=embed_model
#     )
    
#     print("Done! Your knowledge base is ready.")

# if __name__ == "__main__":
#     start_ingestion()



import truststore
truststore.inject_into_ssl()

import os
import ssl
import urllib3
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.cohere import CohereEmbedding

# ביטול אזהרות
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

def start_ingestion():
    # 1. הגדרת מודל ה-Embedding (נשארים עם Cohere כי הוא עבד לך!)
    embed_model = CohereEmbedding(
        api_key=os.environ["COHERE_API_KEY"],
        model_name="embed-multilingual-v3.0",
    )

    # 2. טעינת המסמכים מהתיקייה שלך
    print("Loading documents from ./my_project...")
    documents = SimpleDirectoryReader("./my_project", recursive=True).load_data()

    # 3. יצירת האינדקס (כאן הקסם קורה - זה נשמר בזיכרון כרגע)
    print("Indexing documents...")
    index = VectorStoreIndex.from_documents(
        documents, 
        embed_model=embed_model
    )

    # 4. שמירה פיזית על הדיסק בתיקייה שנקראת 'storage'
    # זה יאפשר לקובץ הצ'אט שלך לקרוא את המידע אחר כך
    print("Saving index to disk...")
    index.storage_context.persist(persist_dir="./storage")
    
    print("\n✅ Done! The knowledge base is saved locally in the '/storage' folder.")

if __name__ == "__main__":
    start_ingestion()