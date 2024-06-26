document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const userMessage = document.getElementById('message').value;
        if (userMessage.trim() === '') return;

        // Display user message in chat box
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user');
        userMessageDiv.textContent = `You: ${userMessage}`;
        chatBox.appendChild(userMessageDiv);

        // Clear the input field
        document.getElementById('message').value = '';

        // Send the message to the server
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        const result = await response.json();
        const chatgptResponse = result.response;

        // Display ChatGPT response in chat box
        const chatgptMessageDiv = document.createElement('div');
        chatgptMessageDiv.classList.add('message', 'chatgpt');
        chatgptMessageDiv.textContent = `ChatGPT: ${chatgptResponse}`;
        chatBox.appendChild(chatgptMessageDiv);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});


