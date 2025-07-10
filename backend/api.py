from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate required environment variables
REQUIRED_VARS = ["IONOS_API_KEY", "IONOS_CHAT_MODEL_ID", "IONOS_IMAGE_MODEL_ID"]
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

IONOS_API_KEY = os.getenv("IONOS_API_KEY")
IONOS_CHAT_MODEL_ID = os.getenv("IONOS_CHAT_MODEL_ID")
IONOS_IMAGE_MODEL_ID = os.getenv("IONOS_IMAGE_MODEL_ID")

CHAT_URL = f"https://inference.de-txl.ionos.com/models/{IONOS_CHAT_MODEL_ID}/predictions"
IMAGE_URL = "https://openai.inference.de-txl.ionos.com/v1/images/generations"

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# 🔁 Helper for IONOS requests
def send_ionos_request(url, payload):
    headers = {
        "Authorization": f"Bearer {IONOS_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        print("🔻 Sending payload to:", url)
        print("📤 Payload:", payload)

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Raw response:", response.text)  # Optional: preview raw response
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP error:", http_err)
        print("📄 Response text:", response.text)
        return {"error": f"HTTP error: {http_err}", "details": response.text}
    except Exception as e:
        print("❌ General error:", e)
        return {"error": str(e)}

# 🔹 Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    print("🧠 Chat prompt received:", prompt)

    payload = {
    "type": "prediction",
    "properties": {
        "input": prompt,
        "options": {
            "temperature": "0.7",     # ✅ string
            "max_length": "300"       # ✅ string
        }
    }
}

    result = send_ionos_request(CHAT_URL, payload)
    print("📦 Chat result:", result)

    if "properties" in result and "output" in result["properties"]:
        return jsonify({"output": result["properties"]["output"]})
    elif "error" in result:
        return jsonify(result), 500
    else:
        return jsonify({"output": "❌ No output received."}), 500

# 🔹 Image generation endpoint
@app.route("/image", methods=["POST"])
def generate_image():
    prompt = request.get_json().get("prompt", "")
    print("🖼️ Image prompt received:", prompt)

    payload = {
        "model": IONOS_IMAGE_MODEL_ID,
        "prompt": prompt,
        "n": 1,
        "size": "1024*1024",
        "response_format": "b64_json"
    }

    result = send_ionos_request(IMAGE_URL, payload)
    print("📦 Image result:", result)

    if "data" in result and result["data"]:
        return jsonify({"image_base64": result["data"][0]["b64_json"]})
    elif "error" in result:
        return jsonify(result), 500
    else:
        return jsonify({"error": "No image data received"}), 500

# ✅ Entry point
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
