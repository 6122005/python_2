import os
import warnings
from dotenv import load_dotenv

# Suppress some noisy HuggingFace/Chroma warnings for clean output
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def build_rag_chain():
    # 1. Load the PDF
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.pdf")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # 2. Chunk the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    # 3. Create HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 4. Store in ChromaDB vector store
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 5. Create QA Chain
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    class SimpleRAGChain:
        def __init__(self, retriever, llm):
            self.retriever = retriever
            self.llm = llm
            
        def invoke(self, inputs):
            query = inputs["input"]
            # Retrieve documents
            docs = self.retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])
            
            # Formulate prompt
            prompt = (
                "You are an assistant for question-answering tasks.\n"
                "Use the following pieces of retrieved context to answer the question.\n"
                "If you don't know the answer, say that you don't know.\n"
                "Use three sentences maximum and keep the answer concise.\n\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{query}"
            )
            
            # Get response
            response = self.llm.invoke([("user", prompt)])
            return {"answer": response.content}
            
    rag_chain = SimpleRAGChain(retriever, llm)
    return rag_chain

def main():
    load_dotenv()
    print("Initializing LangChain RAG pipeline...")
    rag_chain = build_rag_chain()
    
    print("\n--- LangChain RAG System Ready (Day 58) ---")
    question = "What is the secret password for the RAG system?"
    print(f"\nUser: {question}")
    
    response = rag_chain.invoke({"input": question})
    print(f"Agent: {response['answer']}")

if __name__ == "__main__":
    main()
