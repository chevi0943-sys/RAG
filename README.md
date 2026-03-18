# 🤖 Agentic RAG Assistant for Coding Documentation

An advanced **Retrieval-Augmented Generation (RAG)** system designed to query project documentation. The system integrates **Semantic Search** with **Structured Data Extraction** to provide precise answers for both qualitative and quantitative queries.

## 🚀 Key Features

* **Hybrid Search:** Intelligent routing between **Vector Search (Pinecone/Local)** and **Structured Data (JSON)**.
* **Event-Driven Workflow:** Modern architecture built using **LlamaIndex Workflows**.
* **Self-Healing:** Advanced **Query Rewriting** capabilities that trigger automatically if no relevant information is found.
* **Interactive UI:** A user-friendly chat interface powered by **Gradio**.

## 🛠 Tech Stack

* **Framework:** **LlamaIndex**
* **LLM & Embeddings:** **Cohere (Command-R)**
* **Database:** **JSON / Vector Store**
* **Interface:** **Gradio**

## 📊 Process Architecture
<img width="970" height="734" alt="צילום מסך 2026-03-17 162633" src="https://github.com/user-attachments/assets/90cbd6b2-af30-41b3-95bc-ee14bbc36ab8" />

### Workflow Visualization

*Visual representation of the event-driven retrieval and validation process.*

### 🛡️ Guardrails & Infinite Loop Prevention
The system includes a **Self-Correction Loop** (from `validate` to `rewrite_query`). 

> **Note:** This is managed by a **Retry Counter** limited to **3 attempts**. If no relevant information is found after 3 rewrites, the system executes a controlled **StopEvent** to prevent infinite loops and provide a clear "information not found" message.

---

## 📖 How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Extract Data:**
    ```bash
    python extract_data.py
    ```
3.  **Run Assistant:**
    ```bash
    python workflow_chat.py
    ```
