import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# -----------------------
# Paths
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "tutorial.pdf")
db_path = os.path.join(BASE_DIR, "chroma_db")

# -----------------------
# Read PDF
# -----------------------

reader = PdfReader(pdf_path)       

text = ""

for page in reader.pages:

    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

# -----------------------
# Clean
# -----------------------

text = text.replace("\n", " ")

# -----------------------
# Chunk
# -----------------------

def fixed_chunk(text, size=500):

    return [

        text[i:i+size]

        for i in range(0, len(text), size)

    ]

chunks = fixed_chunk(text)

# -----------------------
# Embedding Model
# -----------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

# -----------------------
# ChromaDB
# -----------------------

client = chromadb.PersistentClient(
    path=db_path
)

collection = client.get_or_create_collection(
    name="pdf_collection"
)

# -----------------------
# Store
# -----------------------

for i, chunk in enumerate(chunks):

    collection.upsert(

        ids=[str(i)],

        documents=[chunk],

        embeddings=[embeddings[i].tolist()]

    )

# -----------------------
# Question
# -----------------------

question = input("Ask : ")

question_embedding = model.encode(question)

results = collection.query(

    query_embeddings=[
        question_embedding.tolist()
    ],

    n_results=2

)

print("\nRelevant Chunks:\n")

for doc in results["documents"][0]:

    print(doc)