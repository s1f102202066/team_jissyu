from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import openai
import os
import requests

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

# Function to get restaurant recommendations from Hot Pepper API
def get_restaurant_recommendations(query):
    api_key = os.getenv('HOTPEPPER_API_KEY')
    url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=de36c96caa8a139d&lat=34.67&lng=135.52&range=5&order=4'
    params = {
        'key': api_key,
        'format': 'json',
        'keyword': query,
        'count': 5  # Number of results to return
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', {}).get('shop', [])
        recommendations = []
        for shop in results:
            recommendations.append({
                'name': shop.get('name'),
                'address': shop.get('address'),
                'url': shop.get('urls', {}).get('pc')
            })
        return recommendations
    else:
        return []

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Use OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. If the user asks for restaurant recommendations, suggest some based on their criteria."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000
    )

    chatgpt_response = response['choices'][0]['message']['content'].strip()

    # Check if the response should include restaurant recommendations
    if "recommend" in user_message.lower():
        recommendations = get_restaurant_recommendations(user_message)
        if recommendations:
            recommendation_text = "Here are some restaurant recommendations based on your query:\n"
            for rec in recommendations:
                recommendation_text += f"- {rec['name']}: {rec['address']} (More info: {rec['url']})\n"
            chatgpt_response += "\n\n" + recommendation_text
        else:
            chatgpt_response += "\n\nSorry, I couldn't find any matching restaurants."

    return jsonify({'response': chatgpt_response})

if __name__ == '__main__':
    app.run(debug=True)

