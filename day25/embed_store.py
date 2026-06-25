from extract import extract_text
from sentence_transformers import SentenceTransformer
import chromadb


def fixed_chunk(text, size=500):

    return [
        text[i:i + size]
        for i in range(0, len(text), size)
    ]


pdf_path = "tutorial.pdf"

text = extract_text(pdf_path)

chunks = fixed_chunk(text)

print(f"Total Chunks: {len(chunks)}")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    chunks
).tolist()

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="notes"
)

existing = collection.count()

if existing > 0:

    collection.delete(
        ids=[
            str(i)
            for i in range(existing)
        ]
    )

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[
        str(i)
        for i in range(
            len(chunks)
        )
    ]
)

print("\nEmbeddings Stored Successfully")