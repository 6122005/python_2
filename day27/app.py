from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# -----------------------
# Read PDF
# -----------------------

reader = PdfReader("tutorial.pdf")       

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
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_collection"
)

# -----------------------
# Store
# -----------------------

for i, chunk in enumerate(chunks):

    collection.add(

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