import streamlit as st
from generator import build_qa_chain
from ingestion import document_load, text_split, create_store
import tempfile
from langchain.vectorstores import Chroma

# -------------------------------
# UI CONFIG
# -------------------------------
st.set_page_config(page_title="AI Knowledge Assistant", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
    .chat-bubble-user {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #E8EAF6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Knowledge Assistant")
st.write("Upload documents and chat with your private AI assistant 📚")

# -------------------------------
# SIDEBAR - DATABASE CONTROLS
# -------------------------------
st.sidebar.header("⚡ Database Controls")

if st.sidebar.button("Refresh Database (Clear Previous PDFs)"):
    db = Chroma(persist_directory="vector_store")  # must match your create_store persist_dir
    db.delete_collection()  # clears all previous embeddings
    st.sidebar.success("✅ Vector database cleared! You can upload a new PDF now.")

# -------------------------------
# SIDEBAR - FILE UPLOAD
# -------------------------------
st.sidebar.header("📂 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    docs = []
    for uploaded_file in uploaded_files:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name
            docs.extend(document_load(file_path))
    
    st.sidebar.success(f"✅ Loaded {len(docs)} pages")
    
    # Split and create vector store
    chunks = text_split(docs)
    vs = create_store(chunks, persist_dir="vector_store")
    st.sidebar.info("✅ Vector store updated!")

# -------------------------------
# BUILD QA CHAIN
# -------------------------------
qa_chain = build_qa_chain()

# -------------------------------
# CHAT INTERFACE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Type your question here...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.spinner("🤔 Thinking..."):
        result = qa_chain.invoke({"query": query})
    
    answer = result["result"]
    sources = result.get("source_documents", [])
    
    # Add bot message
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

# Render chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>{msg['content']}</div>", unsafe_allow_html=True)
        
        if msg.get("sources"):
            with st.expander("📌 Sources"):
                for doc in msg["sources"]:
                    st.write("-", doc.page_content[:200] + "...")
