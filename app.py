from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = 'T52k19ishQNb31Xp_E0fLGFSIUB8YphDc5CaN2p11kjqAMvCRCBYi2HeOBnGxBkVHb055gjl_NS5suSKD6SI2LQ'


# 飲食店をおすすめするエンドポイント
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    location = data.get('location', '')
    preferences = data.get('preferences', '')

    # OpenAI APIを使って飲食店をおすすめ
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"旅行客におすすめの飲食店を教えてください。場所: {location}、好み: {preferences}",
        max_tokens=150
    )

    recommendations = response.choices[0].text.strip()
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
