document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');

    // 初回メッセージを表示
    const initialMessageDiv = document.createElement('div');
    initialMessageDiv.classList.add('message', 'chatgpt');
    initialMessageDiv.textContent = 'あなたがお探しの飲食店の条件を教えてください。';
    chatBox.appendChild(initialMessageDiv);

    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault(); // フォームのデフォルトの送信を防止

            const userMessage = document.getElementById('message').value;
            if (userMessage.trim() === '') return; // ユーザーが空白メッセージを送信しないように

            // ユーザーメッセージをチャットボックスに表示
            const userMessageDiv = document.createElement('div');
            userMessageDiv.classList.add('message', 'user');
            userMessageDiv.textContent = `You: ${userMessage}`;
            chatBox.appendChild(userMessageDiv);

            // 入力フィールドをクリア
            document.getElementById('message').value = '';

            try {
                // サーバーにメッセージを送信
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                const chatgptResponse = result.response;

                // ChatGPTの応答をチャットボックスに表示
                const chatgptMessageDiv = document.createElement('div');
                chatgptMessageDiv.classList.add('message', 'chatgpt');

                // 応答を改行ごとに分割して処理
                const lines = chatgptResponse.split('\n');
                lines.forEach(line => {
                    if (line.startsWith('画像: ')) {
                        const imgUrl = line.replace('画像: ', '').trim();
                        const imgElement = document.createElement('img');
                        imgElement.src = imgUrl;
                        imgElement.alt = 'Restaurant Image';
                        imgElement.classList.add('restaurant-image');
                        chatgptMessageDiv.appendChild(imgElement);
                    } else {
                        const textNode = document.createElement('p');
                        textNode.textContent = line;
                        chatgptMessageDiv.appendChild(textNode);
                    }
                });

                chatBox.appendChild(chatgptMessageDiv);

                // チャットボックスをスクロールして最新メッセージを表示
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    } else {
        console.error('chatForm element not found');
    }
});