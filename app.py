from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    notes = data["notes"]
    prompt_type = data["type"]

    # Create prompts
    if prompt_type == "summary":
        prompt = f"""
        Summarize these notes in simple bullet points:

        {notes}
        """

    elif prompt_type == "quiz":
        prompt = f"""
        Generate 3 multiple choice questions with 4 options each.
        Also provide the correct answer.

        Notes:
        {notes}
        """

    elif prompt_type == "flashcards":
        prompt = f"""
        Generate 4 flashcards in this format:

        Q: question
        A: answer

        Notes:
        {notes}
        """

    else:
        prompt = notes

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        text = result["response"]

        return jsonify({"result": text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "result": f"Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)