import chromadb
from sentence_transformers import SentenceTransformer
import uuid


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add_chunks(self, chunks, filename):
        embeddings = self.embedding_model.encode(
            chunks
        ).tolist()

        ids = [
            f"{filename}_{uuid.uuid4()}"
            for _ in chunks
        ]

        metadatas = [
            {
                "filename": filename,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query, top_k=3, filename=None):
        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        where_filter = None

        if filename:
            where_filter = {
                "filename": filename
            }

        if where_filter:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_filter
            )
        else:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        sources = []

        for doc, meta in zip(documents, metadatas):
            sources.append({
                "filename": meta.get("filename"),
                "chunk_index": meta.get("chunk_index"),
                "content": doc
            })

        return sources
    def delete_by_filename(self, filename):
        results = self.collection.get(
            where={
                "filename": filename
            }
        )

        ids = results.get("ids", [])

        if ids:
            self.collection.delete(
                ids=ids
            )   