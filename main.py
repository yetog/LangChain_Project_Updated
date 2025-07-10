from agents.assistant_agent import create_assistant

tools = create_assistant()

# Run chat tool
chat_response = tools[0].func("Give me 3 ideas for eco-friendly drone startups.")
print("🤖 Chat Response:", chat_response)

# Run image tool
image_response = tools[1].func("A futuristic drone delivering medicine in the rainforest")
print("🖼️ Image Response:", image_response)
