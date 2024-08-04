import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

app = Flask(__name__)

# Set your Gemini API key here or load from an environment variable
GOOGLE_API_KEY =os.getenv('GEMINI_API_KEY','AIzaSyAP5FAWvJU5HQLY620SthdIUtvLYnmwRqQ')
genai.configure(api_key=GOOGLE_API_KEY)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Store conversation history
conversation_history = []

@app.route("/", methods=['GET', 'POST'])
def index():
    global conversation_history
    if request.method == 'POST':
        prompt = request.form['prompt']
        logger.info(f"Received prompt: {prompt}")

        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            response_text = response.text
            logger.info(f"Gemini Response: {response_text}")
            conversation_history.append({'user': prompt, 'bot': response_text})
            result = {'success': True, 'response': response_text}
        except Exception as e:
            error_message = f"Error communicating with Gemini API: {e}"
            logger.error(error_message)
            result = {'success': False, 'error': error_message}

        return jsonify(result)

    return render_template('index.html', conversation_history=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)





