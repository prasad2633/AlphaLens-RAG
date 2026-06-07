from dotenv import load_dotenv
from google import genai
import os
from utils.RetryWrapper import retry_on_failure
from langchain_ollama import ChatOllama

load_dotenv()


class AnswerSimplifierModels:

    @retry_on_failure()
    @staticmethod
    def geminiAnswerSimplifier(model_output):
        """
        Simplifies the answer generated from the gemini and refines it and gives a readable answer
        """

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = f"""
        You are an expert technical writer.
        From the given data below can you follow these rules and generate the output

        Rules:
        - Maximum 300 words.
        - Focus on the most important concepts.
        - Do not explain every implementation detail.
        - Avoid repeating information.
        - Use simple language.
        - Keep it more structured so that a human can understand better (points help)

        Preserve all important facts.

        Data: 
        {model_output}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        return response.text

    @staticmethod
    def gemmaAnswerSimplifier(model_output):
        """
        Simplifies the answer generated from the gemma and refines it and gives a readable answer
        """

        prompt = f"""
        You are an expert technical writer.
        From the given data below can you follow these rules and generate the output

        Rules:
        - Maximum 300 words.
        - Focus on the most important concepts.
        - Do not explain every implementation detail.
        - Avoid repeating information.
        - Use simple language.
        - Keep it more structured so that a human can understand better (points help)

        Preserve all important facts.

        Data: 
        {model_output}
        """

        model = ChatOllama(model="gemma3:latest")
        response = model.invoke(prompt)

        return response.content
