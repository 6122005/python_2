from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages[:5]:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def fixed_chunk(text, size=500):

    return [
        text[i:i + size]
        for i in range(0, len(text), size)
    ]


print("=" * 60)
print("NOTE SEARCH TOOL")
print("=" * 60)

pdf_path = "tutorial.pdf"

text = extract_text(pdf_path)

chunks = fixed_chunk(text)

print(
    f"\nLoaded {len(chunks)} chunks"
)

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
    "notes"
)

if collection.count() == 0:

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

while True:

    query = input(
        "\nAsk Question (exit to quit): "
    )

    if query.lower() == "exit":
        break

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=3
    )

    print("\nTop Results\n")

    for i, doc in enumerate(
            results["documents"][0], 1):

        print(f"\nResult {i}")
        print("-" * 40)
        print(doc[:500])