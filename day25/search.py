from sentence_transformers import SentenceTransformer
import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="notes"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

query = input(
    "\nAsk Question: "
)

query_embedding = model.encode(
    query
).tolist()

results = collection.query(
    query_embeddings=[
        query_embedding
    ],
    n_results=3
)

print("\n" + "=" * 60)
print("TOP MATCHES")
print("=" * 60)

for i, doc in enumerate(
        results["documents"][0], 1):

    print(f"\nMatch {i}")
    print("-" * 40)
    print(doc[:800])
