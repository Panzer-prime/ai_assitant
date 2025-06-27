from bs4 import BeautifulSoup
import requests
import urllib.parse
from trafilatura import fetch_url, extract
from src.plugin.base_plugin import BasePluging
from src.utils.ai import RAG
    



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
    
    def run(self, query):
        print("do we even run ")
        rag = RAG()
        text = self.scrapp_websites(self.get_links(query))
        chunks = rag.split_into_chunks(text, sentences_per_chunk=4)


        embeddings = rag.embed_text(chunks)

  
        index = rag.build_index(embeddings)
        top_chunks = rag.search(query, index, chunks, top_k=5)

        return top_chunks


