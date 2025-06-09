from sentence_transformers import SentenceTransformer  # type: ignore
import numpy as np
import faiss

class RAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str):
        chunks = [chunk.strip() for chunk in text.split(".") if chunk.strip()]
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        return chunks, embeddings

    def build_index(self, embeddings):
        embedding_matrix = np.array(embeddings)

        faiss.normalize_L2(embedding_matrix)  
        index = faiss.IndexFlatIP(embedding_matrix.shape[1])  
        index.add(embedding_matrix)
        return index

    def search(self, query: str, index, chunks, top_k=5):
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding) 

        distances, indices = index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            results.append(chunks[idx])
        return results


