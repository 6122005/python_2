from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import SentenceTransformerEmbeddings

from langchain_chroma import Chroma

import os
import google.generativeai as genai
from dotenv import load_dotenv


# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

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

    docs = create_chunks(text)

    db = Chroma.from_documents(

        docs,

        embedding,

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

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text