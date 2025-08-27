from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def document_load(file_path:str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def text_split(documents,chunk_size=500,chunk_overlap=50):
    splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    chunks=splitter.split_documents(documents)
    return chunks

def create_store(chunks,persist_dir="vector_store"):
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore=Chroma.from_documents(documents=chunks,embedding=embedding_model,persist_directory=persist_dir)
    return vectorstore

# if __name__=="__main__":
#     docs=document_load()
#     print(f"Loaded {len(docs)} documents")
#     chunks=text_split(docs)
#     print(f"Split into {len(chunks)} chunks")
#     vs=create_store(chunks)
#     print(f"Created vector store with {len(chunks)} chunks")