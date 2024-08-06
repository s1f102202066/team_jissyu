document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');

    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log("Form submitted");

            const userMessage = document.getElementById('message').value;
            if (userMessage.trim() === '') return;
            console.log("User message:", userMessage);

            // Display user message in chat box
            const userMessageDiv = document.createElement('div');
            userMessageDiv.classList.add('message', 'user');
            userMessageDiv.textContent = `You: ${userMessage}`;
            chatBox.appendChild(userMessageDiv);

            // Clear the input field
            document.getElementById('message').value = '';

            try {
                // Send the message to the server
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
                console.log("ChatGPT response:", chatgptResponse);

                // Display ChatGPT response in chat box
                const chatgptMessageDiv = document.createElement('div');
                chatgptMessageDiv.classList.add('message', 'chatgpt');
                chatgptMessageDiv.textContent = `ChatGPT: ${chatgptResponse}`;
                chatBox.appendChild(chatgptMessageDiv);

                // Scroll to the bottom of the chat box
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    } else {
        console.error('chatForm element not found');
    }
});




