from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def get_google_api_key():
    key = os.getenv("GOOGLE_API_KEY")

    if not key:
        try:
            import streamlit as st
            if "GOOGLE_API_KEY" in st.secrets:
                key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            pass

    return key


DB_PATH = "chroma_db"

embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.create_documents([text])


def process_pdf(pdf_path):
    text = extract_text(pdf_path)

    if not text.strip():
        return False

    docs = create_chunks(text)

    Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=DB_PATH
    )

    return True


def ask_question(question):
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding
    )

    docs = db.similarity_search(
        question,
        k=3
    )

    if not docs:
        return "I don't know."

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not present in the context,
reply exactly:
"I don't know."

Do not use outside knowledge.

Explain the answer in simple language.

Context:
{context}

Question:
{question}

Answer:
"""

    api_key = get_google_api_key()

    if not api_key:
        return (
            "❌ Error: GOOGLE_API_KEY is missing. "
            "Please add it to your .env file or Streamlit Cloud Secrets."
        )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "I don't know."

    except Exception as e:
        return f"❌ Google AI API Error: {e}"