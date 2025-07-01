import os
import json
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from flask import Flask, request, jsonify
from mistralai.client import MistralClient
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")  # ✅ this was missing
MODEL = "pixtral-12b-2409"

# === Initialize Mistral client and Flask app ===
mistral_client = MistralClient(api_key=MISTRAL_API_KEY)  # ✅ this is correct
app = Flask(__name__)

# === Route 1: Generate interview Q&A ===
@app.route('/generate_qa', methods=['POST'])
def generate_interview_qa():
    data = request.get_json()
    candidate_description = data.get("description", "").strip()

    if not candidate_description:
        return jsonify({"error": "Candidate description is required"}), 400

    prompt = f"""
You are an expert HR interviewer and technical hiring consultant.

Based on the following candidate description, generate a list of 5 interview questions tailored to the candidate’s skills and experience level. Then, provide model answers to those questions, assuming an ideal but honest candidate response.

Candidate description: "{candidate_description}"

Instructions:
- If the candidate is a fresher, ask basic conceptual or academic-level questions.
- If the candidate has experience, ask deep technical and architectural-level questions.
- Keep the questions specific to the mentioned technologies or role (e.g., Python developer, Data Analyst, etc.).
- Keep answers practical, clear, and technically sound.
- Return the result strictly in JSON format like this:

{{
  "candidate_description": "Given candidate description",
  "interview": [
    {{
      "question": "Question 1 text here",
      "answer": "Model answer 1"
    }},
    {{
      "question": "Question 2 text here",
      "answer": "Model answer 2"
    }},
    ...
  ]
}}
"""

    messages = [{"role": "user", "content": prompt}]

    try:
        response = mistral_client.chat(
            model=MODEL,
            messages=messages,
            temperature=0.2,
        )
        output = response.choices[0].message.content.strip()

        # Remove ```json and ``` if wrapped in markdown
        if output.startswith("```json"):
            output = output.replace("```json", "").replace("```", "").strip()

        return jsonify(json.loads(output))

    except json.JSONDecodeError:
        return jsonify({
            "error": "Failed to parse response as JSON",
            "raw_response": output
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# === Route 2: Record + Transcribe from Mic ===
@app.route('/transcribe', methods=['GET'])
def transcribe_answer():
    global transcribed_answer

    print("🎤 Recording... Speak now.")
    recording = sd.rec(int(16000 * 15), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    write("mic_input.wav", 16000, recording)
    print("✅ Recording saved.")

    model = whisper.load_model("base")
    result = model.transcribe("mic_input.wav")

    transcribed_answer = result["text"]
    return jsonify({"transcription": transcribed_answer})
# === Route 3: Evaluate answer ===
@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    global transcribed_answer

    if not transcribed_answer:
        return jsonify({"error": "No transcribed answer available. Please call /transcribe first."}), 400

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Prepare prompt
    prompt = f"""
You are an expert technical interviewer.

Given the following question and the candidate’s answer, evaluate how correct the answer is. Give a brief explanation and a correctness percentage (0–100%).

Question: "{question}"
Candidate Answer: "{transcribed_answer}"

Respond in the following JSON format:

{{
  "question": "...",
  "answer": "...",
  "evaluation": "Brief explanation of correctness",
  "correctness_score": 85
}}
"""

    try:
        response = mistral_client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()

        return jsonify(json.loads(content))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run Flask ===
if __name__ == "__main__":
    app.run(debug=True)
