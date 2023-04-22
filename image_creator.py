import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


def create_image_from_prompt(prompt):
    response = openai.Image.create(prompt=prompt, n=3, size="256x256")
    return response["data"]
