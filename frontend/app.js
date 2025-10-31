const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const statusDiv = document.getElementById('status');

const API_URL = 'http://localhost:8000';

// Add message to chat
function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Update status
function setStatus(text, type = '') {
    statusDiv.textContent = text;
    statusDiv.className = `status ${type}`;
}

// Send text message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    messageInput.value = '';
    setStatus('Processing...', 'processing');

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage(data.response, false);
        setStatus('');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Error: Could not connect to server', false);
        setStatus('Error connecting to server');
    }
}

// Handle voice conversation
async function startVoiceConversation() {
    voiceBtn.disabled = true;
    voiceBtn.classList.add('recording');
    setStatus('Listening... Speak now and pause for 3 seconds when done', 'recording');

    try {
        const response = await fetch(`${API_URL}/voice`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            addMessage(data.user_message, true);
            addMessage(data.agent_response, false);
            setStatus('');
        } else {
            setStatus('No speech detected. Try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        setStatus('Error during voice conversation');
    } finally {
        voiceBtn.disabled = false;
        voiceBtn.classList.remove('recording');
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
voiceBtn.addEventListener('click', startVoiceConversation);

// Initial greeting
addMessage('Hello! I am your Smart Calendar Assistant. You can type or use voice to manage appointments.', false);
setStatus('Ready');
