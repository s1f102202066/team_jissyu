from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models  # Import models

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to render the chat interface
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Use OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150
    )

    chatgpt_response = response['choices'][0]['message']['content'].strip()
    return jsonify({'response': chatgpt_response})

if __name__ == '__main__':
    app.run(debug=True)

