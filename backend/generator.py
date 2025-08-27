import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline


def load_vector_store(persist_dir="vector_store"):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    return vectorstore


def build_qa_chain():
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


    generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=512,
        temperature=0.1
    )

    llm = HuggingFacePipeline(pipeline=generator)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    return qa_chain


# if __name__ == "__main__":
#     qa_chain = build_qa_chain()

#     query = "What google wants?"
#     result = qa_chain.invoke({"query": query})

#     print("\n🔹 User Question:", query)
#     print("🔹 Answer:", result["result"])

#     print("\n📌 Sources used:")
#     for doc in result["source_documents"]:
#         print("-", doc.metadata.get("source", "Unknown"))
