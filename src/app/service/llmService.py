from typing import Optional
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from app.service.Expense import Expense
from langchain_core.utils.function_calling import convert_to_openai_tool
from dotenv import load_dotenv, dotenv_values

class LLMService:
    def __init__(self):
        load_dotenv()
        self.apiKey = os.getenv('OPENAI_API_KEY')
        self._runnable = None   # 👈 IMPORTANT

    def _init_llm(self):
        if self._runnable is None:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert extraction algorithm."),
                ("human", "{text}")
            ])

            llm = ChatMistralAI(
                api_key=self.apiKey,
                model="mistral-large-latest",
                temperature=0
            )

            self._runnable = prompt | llm.with_structured_output(schema=Expense)

    def runLLM(self, message):
        self._init_llm()        # 👈 INIT ONLY WHEN NEEDED
        return self._runnable.invoke({"text": message})
