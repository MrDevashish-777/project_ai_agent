/**
 * Chat Functionality
 * Handles chat messages, sending, and receiving
 */

const BASE = 'http://127.0.0.1:8000';
let userPreferences = { nights: null, budget: null, visitors: null };
let hotelSuggestions = {};

/**
 * Send a chat message
 * @param {string} message - The message to send
 */
function sendChat(message) {
    if (!message || !message.trim()) return;
    
    const input = document.getElementById('chat-input');
    
    // Use enhanced message display if available, fallback to regular
    if (typeof addMessageWithAnimation === 'function') {
        addMessageWithAnimation(message, 'user');
    } else {
        addMessage(message, 'user');
    }
    
    input.value = '';
    
    showTypingIndicator();
    const payload = { user_id: getUserId(), message };
    
    fetch(`${BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(r => r.json())
        .then(data => {
            hideTypingIndicator();
            
            // Use enhanced message display if available, fallback to regular
            if (typeof addMessageWithAnimation === 'function') {
                addMessageWithAnimation(data.reply, 'bot', { suggestions: data.suggestions || [] });
            } else {
                addMessage(data.reply, 'bot', { suggestions: data.suggestions || [] });
            }
            
            // Update user preferences
            if (data.meta) {
                if (data.meta.nights) userPreferences.nights = data.meta.nights;
                if (data.meta.visitors) userPreferences.visitors = data.meta.visitors;
            }
            
            // Update budget from suggestions
            if (data.suggestions && data.suggestions.length > 0) {
                data.suggestions.forEach(s => {
                    if (s.price_per_night) userPreferences.budget = s.price_per_night;
                });
            }
        })
        .catch(err => {
            hideTypingIndicator();
            addMessage('⚠️ Error connecting to server: ' + (err.message || err), 'bot');
            showNotification('Connection error! Please try again.', 'error');
        });
}

/**
 * Initialize chat event listeners
 */
function initChatListeners() {
    const icon = document.getElementById('chatbot-icon');
    const chatWindow = document.getElementById('chat-window');
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('chat-input');
    
    // Toggle chat window
    icon.onclick = () => {
        const isVisible = chatWindow.style.display === 'flex';
        if (isVisible) {
            closeChat();
        } else {
            openChat();
        }
    };
    
    // Send button click
    sendBtn.onclick = () => {
        const message = input.value.trim();
        if (message) {
            // Add loading state to button
            sendBtn.classList.add('btn-loading');
            sendBtn.disabled = true;
            
            sendChat(message);
            
            // Remove loading state after a delay
            setTimeout(() => {
                sendBtn.classList.remove('btn-loading');
                sendBtn.disabled = false;
            }, 1000);
        }
    };
    
    // Enter key to send
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = input.value.trim();
            if (message) {
                sendChat(message);
            }
        }
    });
    
    // Add input focus effects
    input.addEventListener('focus', () => {
        input.parentElement.style.boxShadow = '0 0 0 3px rgba(44, 90, 160, 0.1)';
    });
    
    input.addEventListener('blur', () => {
        input.parentElement.style.boxShadow = '';
    });
}

/**
 * Initialize chat on page load
 */
function initializeChat() {
    initChatListeners();
    // Send initial greeting
    sendChat('Hi');
}

/**
 * Enhanced message display with animations
 */
function addMessageWithAnimation(message, sender, options = {}) {
    const chatBody = document.getElementById('chat-body');
    const messageDiv = document.createElement('div');
    messageDiv.className = `msg ${sender}`;
    messageDiv.textContent = message;
    
    // Add animation class
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    
    chatBody.appendChild(messageDiv);
    
    // Trigger animation
    setTimeout(() => {
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
        messageDiv.style.transition = 'all 0.3s ease-out';
    }, 10);
    
    // Add suggestions if provided
    if (options.suggestions && options.suggestions.length > 0) {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggestions';
        
        options.suggestions.forEach((suggestion, index) => {
            hotelSuggestions[suggestion.id] = suggestion;
            
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'suggestion';
            suggestionDiv.innerHTML = `
                <div>
                    <strong>${suggestion.name}</strong><br>
                    <span class="meta">₹${suggestion.price_per_night}/night - ${suggestion.area}</span>
                </div>
                <div class="s-actions">
                    <button onclick="bookHotel('${suggestion.id}')">Book</button>
                    <button onclick="viewDetails('${suggestion.id}')">Details</button>
                </div>
            `;
            
            // Add staggered animation
            suggestionDiv.style.opacity = '0';
            suggestionDiv.style.transform = 'translateX(-20px)';
            suggestionsDiv.appendChild(suggestionDiv);
            
            setTimeout(() => {
                suggestionDiv.style.opacity = '1';
                suggestionDiv.style.transform = 'translateX(0)';
                suggestionDiv.style.transition = 'all 0.3s ease-out';
            }, 200 + (index * 100));
        });
        
        chatBody.appendChild(suggestionsDiv);
    }
    
    chatBody.scrollTop = chatBody.scrollHeight;
}
