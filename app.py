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
    url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    params = {
        'key': api_key,
        'format': 'json',
        'keyword': query,
        'large_area': 'Z011',  # 東京エリアを指定（Z011は東京エリアのコード）
        'count': 5  # 返す結果の数
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', {}).get('shop', [])
        recommendations = []
        for shop in results:
            recommendations.append({
                'name': shop.get('name'),
                'address': shop.get('address'),
                'url': shop.get('urls', {}).get('pc'),
                'image_url': shop.get('photo', {}).get('pc', {}).get('l') 
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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. No matter the topic, you always relate the conversation back to restaurants or food recommendations."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000
    )

    chatgpt_response = response['choices'][0]['message']['content'].strip()

    # Always include restaurant recommendations based on user's message
    recommendations = get_restaurant_recommendations(user_message)
    if recommendations:
        recommendation_text = ""
        for rec in recommendations:
            recommendation_text += f"- 店名: {rec['name']}\n  住所: {rec['address']}\n  詳細: {rec['url']}\n  画像: {rec['image_url']}\n\n"
        chatgpt_response += "\n\n" + recommendation_text.strip()
    else:
        # If no restaurants are found, suggest thinking about food anyway
        chatgpt_response += "\n\nところで、美味しい飲食店をお探しではありませんか？どんな話題でも食事に関する情報をご提供いたします。"

    return jsonify({'response': chatgpt_response})

if __name__ == '__main__':
    app.run(debug=True)



