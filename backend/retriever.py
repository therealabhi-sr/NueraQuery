from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def load_vector_store(persist_dir="vector_store"):
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore=Chroma(persist_directory=persist_dir,embedding_function=embedding_model)
    return vectorstore

def retrieve_relevant_docs(query,top_k=3):
    vectorstore=load_vector_store()
    results=vectorstore.similarity_search(query,k=top_k)
    return results

if __name__=="__main__":
    query="what google wants"
    results=retrieve_relevant_docs(query)
    
    print("Top relevant Chunks")
    
    for i,doc in enumerate(results):
        print(f"chunk{i+1}:")
        print(doc.page_content[:300])
        print("-"*50)