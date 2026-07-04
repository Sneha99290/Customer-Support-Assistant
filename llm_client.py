from langchain_groq import ChatGroq
import os
from config import GROQ_API_KEY, GROQ_MODEL


class LLMClient:
    def __init__(self):
        self.model = GROQ_MODEL
        self.api_key = GROQ_API_KEY

    def create_client(self):
        llm = ChatGroq(model=self.model, api_key=self.api_key, temperature=0.2)
        return llm