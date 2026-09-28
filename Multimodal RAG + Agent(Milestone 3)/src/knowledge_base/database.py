import chromadb
from sentence_transformers import SentenceTransformer

# load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# connect to local chromadb (saves data to disk)
client     = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="knowledge_base"
)


def add_chunks_to_db(chunks, source_name="safety_manual"):
    print(f"Adding {len(chunks)} chunks to database...")

    embeddings = model.encode(chunks).tolist()

    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_id": str(i)} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print("Done! Total documents in DB:", collection.count())


def search(query, top_k=3):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    output = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        output.append({
            "text"    : doc,
            "source"  : meta.get("source", ""),
            "distance": round(dist, 4)
        })
    return output


def reset_db():
    global collection

    try:
        client.delete_collection("knowledge_base")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="knowledge_base"
    )

    print("Database cleared.")

# test
if __name__ == "__main__":
    sample_chunks = [
        "All workers must wear helmets on construction sites.",
        "Safety goggles are needed near chemicals.",
        "Fire extinguishers are on every floor.",
        "First aid kits are near every workstation.",
    ]

    add_chunks_to_db(sample_chunks, source_name="demo")

    print("\nSearch results for: 'helmet requirements'")
    results = search("helmet requirements", top_k=2)
    for r in results:
        print(f"  [{r['distance']}] {r['text']}")

    reset_db()
