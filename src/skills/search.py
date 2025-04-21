from bs4 import BeautifulSoup
import requests
import urllib.parse
import aiohttp
import asyncio


class Search:
    def __init__(self, querry, browser_path = ""):
        self.querry = querry
        self.browser_path = browser_path

    def get_links(self, max_results = 5):
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": self.querry, "kl": "us-en"}

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

    async def scrapp_websites(self, sites):
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            results = await asyncio.gather(*[self.fetch(session, site['url']) for site in sites], return_exceptions=True)

            return [result for result in results if result]


    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout = 5) as response: 
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")

                paragraphs = soup.find_all("p")

                text = "\n".join([p.get_text() for p in paragraphs])

                return text[:5000]

        except Exception as e:
            print(f"[!] Failed to scrape {url} -> {e}")

    
    def search(self):
        return asyncio.run(self.scrapp_websites(self.get_links()))

