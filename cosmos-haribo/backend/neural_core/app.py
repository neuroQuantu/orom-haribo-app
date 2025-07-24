from flask import Flask, request, jsonify
import openai, os
from lava_runner import run_snn_inference
import redis, pinecone

openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-west1")
pine_index = pinecone.Index("haribo-memory")
r = redis.Redis(host='localhost', port=6379)

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    text = request.json["text"]
    vec = openai.embeddings.create(input=text)["data"][0]["embedding"]
    pine_index.upsert([(text, vec)])
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}]
    )
    return jsonify({"reply": response.choices[0].message.content})

@app.route("/sense", methods=["POST"])
def sense():
    features = request.json["features"]
    output = run_snn_inference(features)
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
