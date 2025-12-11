/**
 * Utility Functions
 * Shared helper functions used across the application
 */

/**
 * Get or create a unique user ID
 * @returns {string} User ID
 */
function getUserId() {
    let id = localStorage.getItem('ai_user_id');
    if (!id) {
        id = 'u' + Math.random().toString(36).slice(2, 10);
        localStorage.setItem('ai_user_id', id);
    }
    return id;
}

/**
 * Show a notification message
 * @param {string} message - The message to display
 * @param {boolean} isError - Whether this is an error notification
 */
function showNotification(message, isError = false) {
    const notif = document.getElementById('notification');
    notif.textContent = message;
    notif.className = isError ? 'error' : '';
    notif.style.display = 'block';
    
    setTimeout(() => {
        notif.classList.add('hide');
        setTimeout(() => {
            notif.style.display = 'none';
            notif.classList.remove('hide');
        }, 300);
    }, 3000);
}

/**
 * Add a message to the chat
 * @param {string} text - Message text
 * @param {string} type - Message type ('user' or 'bot')
 * @param {object} meta - Metadata including suggestions
 */
function addMessage(text, type = 'bot', meta = null) {
    const chatBody = document.getElementById('chat-body');
    const div = document.createElement('div');
    const p = document.createElement('div');
    p.className = 'msg ' + (type === 'user' ? 'user' : 'bot');
    p.textContent = text;
    div.appendChild(p);
    
    if (meta && meta.suggestions) {
        const s = document.createElement('div');
        s.className = 'suggestions';
        for (const h of meta.suggestions) {
            const el = createSuggestionItem(h);
            s.appendChild(el);
        }
        div.appendChild(s);
    }
    
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
}

/**
 * Show typing indicator
 * @returns {HTMLElement} The typing indicator element
 */
function showTyping() {
    const chatBody = document.getElementById('chat-body');
    const d = document.createElement('div');
    d.id = 'typing-indicator';
    d.className = 'msg bot typing';
    d.textContent = 'Bot is typing...';
    chatBody.appendChild(d);
    chatBody.scrollTop = chatBody.scrollHeight;
    return d;
}

/**
 * Remove typing indicator
 * @param {HTMLElement} element - The typing indicator element
 */
function removeTyping(element) {
    if (element && element.parentNode) {
        element.parentNode.removeChild(element);
    }
}

/**
 * Create a suggestion item (hotel card)
 * @param {object} hotel - Hotel object with properties
 * @returns {HTMLElement} The suggestion element
 */
function createSuggestionItem(hotel) {
    const card = document.createElement('div');
    card.className = 'suggestion';
    
    const left = document.createElement('div');
    left.innerHTML = `<b>${hotel.name}</b><div class='meta'>id: ${hotel.id} · ₹${hotel.price_per_night} · ⭐${hotel.rating}</div>`;
    
    const actions = document.createElement('div');
    actions.className = 's-actions';
    
    const selectBtn = document.createElement('button');
    selectBtn.textContent = 'Select';
    selectBtn.onclick = () => {
        sendChat(`${hotel.id}`);
    };
    
    const bookBtn = document.createElement('button');
    bookBtn.textContent = 'Book';
    bookBtn.onclick = () => {
        openBookingModal(hotel);
    };
    
    actions.appendChild(selectBtn);
    actions.appendChild(bookBtn);
    card.appendChild(left);
    card.appendChild(actions);
    
    return card;
}
