import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

IONOS_MODEL_ID = os.getenv("IONOS_CHAT_MODEL_ID")
IONOS_API_KEY = os.getenv("IONOS_API_KEY")
IONOS_ENDPOINT = f"https://inference.de-txl.ionos.com/models/{IONOS_MODEL_ID}/predictions"

@tool
def ionos_chat_tool(query: str) -> str:
    """Use the IONOS model to respond to natural language queries."""
    headers = {
        "Authorization": f"Bearer {IONOS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "prediction",
        "properties": {
            "input": query,
            "options": {
                "temperature": "0.7",
                "max_length": "300"
            }
        }
    }

    try:
        response = requests.post(IONOS_ENDPOINT, headers=headers, json=payload)
        return response.json().get("properties", {}).get("output", "❌ No response.")
    except Exception as e:
        return f"Error calling IONOS model: {e}"
