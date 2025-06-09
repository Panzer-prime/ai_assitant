from bs4 import BeautifulSoup
import requests
import urllib.parse
from trafilatura import fetch_url, extract
from src.plugin.base_plugin import BasePluging

from sentence_transformers import SentenceTransformer  # type: ignore
import numpy as np
import faiss
import math
import json

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
    

    def search_cos(self, query, embedings, chunks, top_k = 5):
        query_embeding = self.model.encode([query])
        faiss.normalize_L2(query_embeding)

        results = []
        for i, vec in enumerate(embedings):
            similarity = self.cosine_similarity(query, vec)
            results.append((chunks[i], similarity))

        results.sort(key = lambda x: x[1], reverse=True)[:top_k]
        return results


    def cosine_similarity(self, vec1, vec2):

        sum = 0
        for x, y in zip(vec1, vec2):
            sum += x * y
        
        return sum/ (self.magnitude(vec1) * self.magnitude(vec2))

    def magnitude(self, X):
        sum_squares = 0
        for i in X:
            sum_squares += i ** 2
        
        return math.sqrt(sum_squares)
    



class Search(BasePluging):
    
    def __init__(self):
        self.name = "search"
        self.description = "function that user can use to seach top 5 results of a particular subject on interest e.g searching information about dogs"

    def get_links(self, querry, max_results = 5):
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": querry, "kl": "us-en"}

        response = requests.get("https://html.duckduckgo.com/html", headers=headers, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for a in soup.find_all("a", class_="result__a", limit=max_results):
            title = a.get_text()
            raw_link = a["href"]
            parsed = urllib.parse.urlparse(raw_link)
            actual_url = urllib.parse.parse_qs(parsed.query).get("uddg", [None])[0]
            if actual_url:
                results.append({"title": title, "url": actual_url})

        return results

    def scrapp_websites(self, sites):
        content = ""
        for site in sites:
            result = fetch_url(site["url"])
            text = extract(result)
            content += str(text)

        return content
    
    def run(self, querry):
        print("do we even run ")
        r = RAG()
        text = self.scrapp_websites(self.get_links(querry))

        chunks, embedings = r.embed_text(text)
        index = r.build_index(embedings)
        results =  r.search(querry, index, chunks)
        print(results)
        return results

    def can_run(self,value: str):
        return value == "search"
    
