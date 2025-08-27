NueraQuery 🤖

NueraQuery is an AI-powered document question-answering system that allows users to interact with uploaded documents (PDFs, Word, text, etc.) and get intelligent answers in natural language. It combines state-of-the-art NLP techniques, vector embeddings, and retrieval-based AI to provide fast, accurate, and context-aware responses.

🌟 Features

Upload and analyze multiple types of documents (PDF, DOCX, TXT).

Convert documents into vector embeddings for semantic search.

Ask natural language questions and get instant answers.

Chat-style interface with distinct user and bot message styling.

Built using Python, Streamlit, LangChain, and ChromaDB.

Optimized for resume-worthy portfolio projects.

🏗 Architecture Overview
User <--> Streamlit UI <--> QA Chain <--> Vector Store (ChromaDB) <--> Document Embeddings


Streamlit Frontend:
Provides a simple and interactive chat interface to upload files, ask questions, and view AI responses.

Document Loader & Splitter:
Breaks large documents into smaller, manageable chunks for efficient embedding.

Vector Store (ChromaDB):
Stores embeddings and allows semantic retrieval of relevant document sections.

QA Chain (LangChain + LLM):
Uses retrieval-augmented generation to provide accurate answers based on the document context.

Optional Local Storage:
Caches embeddings and processed data for faster subsequent queries.

🛠 Tech Stack

Python 3.10+

Streamlit – Web-based UI

LangChain – Orchestrating LLM pipelines

ChromaDB – Vector database for embeddings

OpenAI GPT (or similar LLM) – Core language model for answering queries

PyPDF2 / python-docx / textract – Document parsing

FAISS (optional) – Alternative vector store for local search

⚡ Setup & Installation

Clone the repository

git clone https://github.com/therealabhi-sr/NueraQuery.git
cd NueraQuery


Create a virtual environment

python -m venv .venv


Activate the virtual environment

Windows:

.venv\Scripts\activate


Mac/Linux:

source .venv/bin/activate


Install dependencies

pip install -r requirements.txt


Set OpenAI API Key (or your preferred LLM API)

export OPENAI_API_KEY="your_api_key_here"  # Mac/Linux
setx OPENAI_API_KEY "your_api_key_here"     # Windows


Run the Streamlit app

streamlit run app.py

📝 Usage

Open the app in your browser (Streamlit default: http://localhost:8501).

Upload your document(s).

Ask questions in natural language.

Receive answers extracted intelligently from your documents.

Chat interface highlights user and AI responses for readability.

💡 Example Questions

"What is the mission of this company?"

"Summarize the financial highlights of this report."

"List the key team members mentioned in this PDF."

"What technologies are used in this document?"

📂 Folder Structure
NueraQuery/
├── app.py               # Streamlit app
├── backend/
│   ├── generator.py     # QA chain logic
│   ├── ingestion.py     # Document loader, splitter, and vector storage
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation

🚀 Future Improvements

Support for real-time chat with multiple document uploads.

Integration with Google Drive / Dropbox for cloud document access.

Advanced analytics for document insights.

Custom embeddings models for domain-specific knowledge.

🧑‍💻 Author

Abhishek Sr
Aspiring AI/ML Engineer | Portfolio Project: NueraQuery
GitHub
 | LinkedIn

📜 License

MIT License © 2025 Abhishek Sr
