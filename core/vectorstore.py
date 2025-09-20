import chromadb
from chromadb.config import Settings as ChromaSettings

# class VectorStore:
#     def __init__(self, persist_dir: str, collection_name: str = "docs"):
#         self.client = chromadb.Client(ChromaSettings(is_persistent=True, persist_directory=persist_dir))
#         self.col = self.client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str = "docs"):
        self.client = chromadb.Client(ChromaSettings(
            is_persistent=True,
            persist_directory=persist_dir,
            anonymized_telemetry=False,  # << ajoute ça
        ))
        self.col = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, ids, embeddings, metadatas, documents):
        self.col.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def query(self, query_embeddings, top_k: int):
        res = self.col.query(
            query_embeddings=query_embeddings,
            n_results=top_k,
            include=["distances","metadatas","documents"] 
        )
        out = []
        if res and res["ids"]:
            for i in range(len(res["ids"][0])):
                out.append({
                    "id": res["ids"][0][i],
                    "doc": res["documents"][0][i],
                    "metadata": res["metadatas"][0][i],
                    "distance": res["distances"][0][i],
                })
        return out
