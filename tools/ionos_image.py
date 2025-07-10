import os
import base64
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

IONOS_API_KEY = os.getenv("IONOS_API_KEY")

@tool
def ionos_image_tool(prompt: str) -> str:
    """Generate an image using IONOS image model from text prompt."""
    endpoint = "https://openai.inference.de-txl.ionos.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {IONOS_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }
    try:
        response = requests.post(endpoint, json=body, headers=headers).json()
        img_data = base64.b64decode(response["data"][0]["b64_json"])
        output_path = "generated_image.png"
        with open(output_path, "wb") as f:
            f.write(img_data)
        return f"Image saved to {output_path}"
    except Exception as e:
        return f"Image generation failed: {e}"
