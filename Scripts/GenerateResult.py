from google import genai
import os
import json
import base64
from dotenv import load_dotenv
from utils.RetryWrapper import retry_on_failure

load_dotenv()


@retry_on_failure()
def generateFinalAnswer(chunks, query):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        prompt_text = f"""
        Based on the following documents, answer this question:

        QUESTION:
        {query}

        CONTENT TO ANALYZE:
        """

        for i, chunk in enumerate(chunks):
            prompt_text += f"\n---- Document {i+1} ----\n"

            if "original_content" in chunk.metadata:
                original_data = json.loads(chunk.metadata["original_content"])

                raw_text = original_data.get("raw_text", "")

                if raw_text:
                    prompt_text += f"TEXT:\n{raw_text}\n\n"

                tables_html = original_data.get("tables_html", [])

                if tables_html:
                    prompt_text += "TABLES:\n"

                    for j, table in enumerate(tables_html):
                        prompt_text += f"Table {j+1}:\n" f"{table}\n\n"

        prompt_text += """
Please provide a clear and comprehensive answer
using text, tables and images.

If information is insufficient, say:
"I don't have enough information
to answer that question."

ANSWER:
"""

        # Use a heterogeneous list to hold the prompt text and any binary/image parts
        contents = []
        contents.append(prompt_text)

        # Add images
        for chunk in chunks:
            if "original_content" in chunk.metadata:

                original_data = json.loads(chunk.metadata["original_content"])

                images_base64 = original_data.get("images_base64", [])

                for img_b64 in images_base64:

                    contents.append(
                        {"mime_type": "image/jpeg", "data": base64.b64decode(img_b64)}
                    )

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents
        )

        return response.text

    except Exception as e:
        print(f"Answer generation failed: {e}")
        return "Sorry Could not generate answer"
