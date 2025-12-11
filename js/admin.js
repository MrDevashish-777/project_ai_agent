/**
 * Admin Panel Functionality
 * Handles admin login, authentication, and dashboard
 */

let adminToken = null;
let adminChats = {}; // Store chats grouped by user_id

/**
 * Show admin login modal
 */
function showAdminLogin() {
    const modal = document.getElementById('admin-login-modal');
    const username = document.getElementById('admin-username');
    modal.style.display = 'flex';
    username.focus();
}

/**
 * Reset admin login inputs
 */
function resetAdminLoginInputs() {
    document.getElementById('admin-username').value = '';
    document.getElementById('admin-password').value = '';
}

/**
 * Close admin dashboard
 */
function closeAdminDashboard() {
    const dashboard = document.getElementById('admin-dashboard');
    dashboard.style.display = 'none';
    adminToken = null;
    adminChats = {};
}

/**
 * Perform admin login
 */
async function performAdminLogin() {
    const username = document.getElementById('admin-username').value.trim();
    const password = document.getElementById('admin-password').value;
    
    if (!username || !password) {
        showNotification('Please enter username and password', true);
        return;
    }
    
    try {
        const res = await fetch(`${BASE}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (!res.ok) {
            showNotification('Invalid credentials', true);
            return;
        }
        
        const data = await res.json();
        adminToken = data.token;
        
        // Close modal and reset inputs
        if (typeof closeAdminModal === 'function') {
            closeAdminModal();
        } else {
            // Fallback if app.js hasn't loaded or defined it
            document.getElementById('admin-login-modal').style.display = 'none';
        }
        resetAdminLoginInputs();
        
        showAdminDashboard();
        showNotification('Logged in as admin', false);
    } catch (err) {
        showNotification('Login failed: ' + err.message, true);
    }
}

/**
 * Show admin dashboard
 */
async function showAdminDashboard() {
    const dashboard = document.getElementById('admin-dashboard');
    dashboard.style.display = 'flex'; // Changed to flex for layout
    await loadAdminData();
}

/**
 * Load admin data and populate dashboard
 */
async function loadAdminData() {
    try {
        const res = await fetch(`${BASE}/admin/chats?limit=100`, {
            headers: { 'Authorization': `Bearer ${adminToken}` }
        });
        
        if (!res.ok) {
            showNotification('Failed to load admin data', true);
            return;
        }
        
        const data = await res.json();
        
        // Group messages by user_id
        adminChats = {};
        if (data.conversations && data.conversations.length > 0) {
            // Sort by date ascending first to ensure order
            data.conversations.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            
            data.conversations.forEach(msg => {
                if (!adminChats[msg.user_id]) {
                    adminChats[msg.user_id] = {
                        messages: [],
                        lastMessage: msg,
                        userId: msg.user_id
                    };
                }
                adminChats[msg.user_id].messages.push(msg);
                adminChats[msg.user_id].lastMessage = msg; // Update last message
            });
        }
        
        renderChatList();
        
    } catch (err) {
        showNotification('Error loading data: ' + err.message, true);
    }
}

/**
 * Render the list of chats in the sidebar
 */
function renderChatList() {
    const chatList = document.getElementById('admin-chat-list');
    chatList.innerHTML = '';
    
    const userIds = Object.keys(adminChats);
    
    if (userIds.length === 0) {
        chatList.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">No conversations found</div>';
        return;
    }
    
    // Sort users by last message time (descending)
    userIds.sort((a, b) => {
        const timeA = new Date(adminChats[a].lastMessage.created_at);
        const timeB = new Date(adminChats[b].lastMessage.created_at);
        return timeB - timeA;
    });
    
    userIds.forEach(userId => {
        const chat = adminChats[userId];
        const lastMsg = chat.lastMessage;
        const time = new Date(lastMsg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const div = document.createElement('div');
        div.className = 'chat-list-item';
        div.onclick = () => openAdminChat(userId);
        div.id = `chat-item-${userId}`;
        
        div.innerHTML = `
            <div class="chat-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="chat-info">
                <div class="chat-name">User ${userId.substring(0, 8)}...</div>
                <div class="chat-preview">
                    ${lastMsg.role === 'assistant' ? '<i class="fas fa-check-double" style="font-size: 0.7rem; color: #53bdeb;"></i> ' : ''}
                    ${escapeHtml(lastMsg.message)}
                </div>
            </div>
            <div class="chat-meta">${time}</div>
        `;
        
        chatList.appendChild(div);
    });
}

/**
 * Open a specific chat
 */
function openAdminChat(userId) {
    const chatData = adminChats[userId];
    if (!chatData) return;
    
    // Update active state in sidebar
    document.querySelectorAll('.chat-list-item').forEach(el => el.classList.remove('active'));
    const activeItem = document.getElementById(`chat-item-${userId}`);
    if (activeItem) activeItem.classList.add('active');
    
    // Update header
    const headerUser = document.getElementById('current-chat-user');
    headerUser.innerHTML = `<i class="fas fa-user-circle"></i> User ${userId}`;
    
    // Render messages
    const messagesContainer = document.getElementById('admin-chat-messages');
    messagesContainer.innerHTML = '';
    
    chatData.messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `admin-message ${msg.role === 'user' ? 'user' : 'bot'}`;
        
        const time = new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        msgDiv.innerHTML = `
            <div class="message-content">${escapeHtml(msg.message)}</div>
            <div class="message-time">${time}</div>
        `;
        
        messagesContainer.appendChild(msgDiv);
    });
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Helper to escape HTML
 */
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Initialize admin panel event listeners
 */
function initAdminListeners() {
    const adminPanelBtn = document.getElementById('admin-panel-btn');
    const adminLoginBtn = document.getElementById('admin-login-btn');
    const adminCloseBtn = document.getElementById('admin-close-btn');
    const adminLogoutBtn = document.getElementById('admin-logout-btn');
    const adminUsername = document.getElementById('admin-username');
    const adminPassword = document.getElementById('admin-password');
    
    // Admin panel button
    if (adminPanelBtn) {
        adminPanelBtn.onclick = () => {
            showAdminLogin();
        };
    }
    
    // Login button
    if (adminLoginBtn) {
        adminLoginBtn.onclick = () => {
            performAdminLogin();
        };
    }
    
    // Close login button
    if (adminCloseBtn) {
        adminCloseBtn.onclick = () => {
            if (typeof closeAdminModal === 'function') {
                closeAdminModal();
            } else {
                document.getElementById('admin-login-modal').style.display = 'none';
            }
        };
    }
    
    // Logout button
    if (adminLogoutBtn) {
        adminLogoutBtn.onclick = () => {
            closeAdminDashboard();
        };
    }
    
    // Enter key on username
    if (adminUsername) {
        adminUsername.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performAdminLogin();
            }
        });
    }
    
    // Enter key on password
    if (adminPassword) {
        adminPassword.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performAdminLogin();
            }
        });
    }
}
