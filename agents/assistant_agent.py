from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from tools.ionos_chat import ionos_chat_tool
from tools.ionos_image import ionos_image_tool
from dotenv import load_dotenv
import os

load_dotenv()

def create_assistant():
    # Wrap our tools with LangChain Tool interface
    tools = [
        Tool(name="ionos_chat_tool", func=ionos_chat_tool, description="Answer natural language queries using IONOS AI."),
        Tool(name="ionos_image_tool", func=ionos_image_tool, description="Generate images from text using IONOS AI.")
    ]

    # Since we don’t use OpenAI, we don't need a chat model
    # We'll just invoke tools directly from main.py or create a custom chain later

    # For now, return the tools list for manual use
    return tools
