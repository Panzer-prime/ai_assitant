import ollama
from ollama import ChatResponse
import json
import os
import re

from sentence_transformers import SentenceTransformer  # type: ignore
import numpy as np
import faiss
import math


class AI:
    def __init__(self, model, pathToPrompt):

        self.model = model
        self.system_prompt = self.get_system_prompt(pathToPrompt)
        self.model = model
    
    
    def get_system_prompt(self, pathToPrompt):
        if not os.path.exists(pathToPrompt):
            print("couldnt get system prompt make sure the file path is right")
            return ""

        with open(pathToPrompt, "r") as file: 
            return file.read()



    def get_ai_response(self, prompt: str, tools: list, data = ""):
    
        response: ChatResponse = ollama.chat(self.model, messages=[{
            "role": "user",
            "content": prompt + data
        }], tools = tools,
        format="json")

        return response.message.tool_calls or [],  json.loads(response.message.content)





class RAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text):
        embeddings = self.model.encode(text, show_progress_bar=True)
        return embeddings

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
        return [chunks[i] for i in indices[0]]

    def cosine_similarity(self, A, B):
        A = np.array(A)
        B = np.array(B)
        dot_product = np.dot(A, B.T)
        norm_A = np.linalg.norm(A, axis=-1, keepdims=True)
        norm_B = np.linalg.norm(B, axis=-1, keepdims=True)
        return dot_product / (norm_A * norm_B.T)

    def find_most_relevant(self, text_embedding_pairs: list, prompt_embedding: list, top_k: int = 5):
        """
        Finds the most relevant texts by cosine similarity.
        Args:
            text_embedding_pairs (list): List of (text, embedding) tuples.
            prompt_embedding (list): The embedding of the prompt.
            top_k (int): Number of top texts to return.
        Returns:
            list: Top-k most relevant texts.
        """
        texts, embeddings = zip(*text_embedding_pairs)
        distances = self.cosine_similarity([prompt_embedding], embeddings)[0]
        top_similar = np.argsort(distances)[-top_k:][::-1]
        return [texts[i] for i in top_similar]

    def split_into_sentences(self, text: str):
        alphabets = "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\\s|She\\s|It\\s|They\\s|Their\\s|Our\\s|We\\s|But\\s|However\\s|That\\s|This\\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov|edu|me)"
        digits = "([0-9])"
        multiple_dots = r'\.{2,}'
        
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
        text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
        text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
        text = text.replace(".\"", "\".")
        text = text.replace("!\"", "\"!")
        text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def split_into_chunks(self, text: str, sentences_per_chunk: int):
        """
        Split the text into chunks, each containing a max number of sentences.
        Args:
            text (str): Input text.
            sentences_per_chunk (int): Number of sentences per chunk.
        Returns:
            list: List of text chunks.
        """
        sentences = self.split_into_sentences(text)
        return [" ".join(sentences[i:i + sentences_per_chunk]) for i in range(0, len(sentences), sentences_per_chunk)]
    


