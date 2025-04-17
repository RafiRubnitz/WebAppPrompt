'''
llm.py
This module response for the LLM (Large Language Model) interactions.
It contains the LLM class, which is an abstract base class for all LLMs.
all LLMs should inherit from this class and implement the required methods.
'''

from abc import ABC, abstractmethod
from typing import Any
from groq import Groq

class LLM(ABC):

    @abstractmethod
    def __init__(self, api_key: str,model: str):
        """
        Initialize the LLM with the given API key.
        """
        pass

    @abstractmethod
    def chat(self, messages: Any) -> str:
        """
        Generate a chat response based on the given messages.
        """
        pass


class GroqLLM(LLM):
    """
    A wrapper class for the Groq LLM.
    """

    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def chat(self, messages: Any) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

def create_llm(llm_name: str,api_key: str, model: str) -> LLM:
    """
    Factory function to create an LLM instance based on the specified model.
    """
    if llm_name == "groq":
        return GroqLLM(api_key=api_key, model=model)
    else:
        raise ValueError(f"Unsupported model: {llm_name}")
