from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import SentenceTransformerEmbeddings

from langchain_chroma import Chroma

import ollama


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

Answer only using the context below.

If answer is not found,

say "I don't know."

Context:

{context}

Question:

{question}

Answer:

"""

    response = ollama.chat(

        model="gemma3:1b",

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )

    return response["message"]["content"]