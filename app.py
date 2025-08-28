import streamlit as st
from backend.generator import build_qa_chain
from backend.ingestion import document_load, text_split, create_store
import tempfile
import os

# -------------------------------
# UI CONFIG
# -------------------------------
st.set_page_config(page_title="NueraQuery", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
    .chat-bubble-user {
        background-color: #4CAF50; /* brighter green */
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
        max-width: 80%;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        font-weight: 500;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-bubble-bot {
        background-color: #2196F3; /* bright blue */
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: left;
        max-width: 80%;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        font-weight: 500;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🤖 NueraQuery")
st.write("AI-Powered Knowledge Assistant for Enterprise Data Retrieval 📚")

# -------------------------------
# SIDEBAR - FILE UPLOAD
# -------------------------------
st.sidebar.header("📂 Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    docs = []
    for uploaded_file in uploaded_files:
        # Save to temp file safely
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name
        # Load documents from the temp file
        docs.extend(document_load(file_path))
    
    st.sidebar.success(f"✅ Loaded {len(docs)} pages")
    
    # Split into chunks and create vector store
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

# Input box at bottom
query = st.chat_input("Type your question here...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.spinner("🤔 Thinking..."):
        result = qa_chain.invoke({"query": query})
    print(result)
    answer = result.get("result", "")
    sources = result.get("source_documents", [])
    
    # Add bot message
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

# Render chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>{msg['content']}</div>", unsafe_allow_html=True)
        
        if msg.get("sources"):
            with st.expander("📌 Sources"):
                for doc in msg["sources"]:
                    st.write("-", doc.page_content[:200].replace("\n", " ") + "...")

