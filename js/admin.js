/**
 * Admin Panel Functionality
 * Handles admin login, authentication, and dashboard
 */

let adminToken = null;

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
 * Close admin login modal
 */
function closeAdminLogin() {
    const modal = document.getElementById('admin-login-modal');
    modal.style.display = 'none';
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
        closeAdminLogin();
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
    dashboard.style.display = 'block';
    await loadAdminData();
}

/**
 * Load admin data and populate dashboard
 */
async function loadAdminData() {
    try {
        const res = await fetch(`${BASE}/admin/chats?limit=20`, {
            headers: { 'Authorization': `Bearer ${adminToken}` }
        });
        
        if (!res.ok) {
            showNotification('Failed to load admin data', true);
            return;
        }
        
        const data = await res.json();
        const tbody = document.getElementById('admin-chats-tbody');
        tbody.innerHTML = '';
        
        if (data.conversations && data.conversations.length > 0) {
            const uniqueUsers = new Set(data.conversations.map(c => c.user_id));
            document.getElementById('admin-total-chats').textContent = data.count;
            document.getElementById('admin-active-users').textContent = uniqueUsers.size;
            
            data.conversations.forEach(conv => {
                const row = document.createElement('tr');
                const timestamp = conv.created_at 
                    ? new Date(conv.created_at).toLocaleString() 
                    : 'N/A';
                const preview = (conv.message || '')
                    .substring(0, 60)
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                
                row.innerHTML = `
                    <td>${conv.user_id}</td>
                    <td><strong>${conv.role}</strong></td>
                    <td>${preview}${preview.length > 60 ? '...' : ''}</td>
                    <td>${timestamp}</td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px;">No conversations found</td></tr>';
        }
    } catch (err) {
        showNotification('Error loading data: ' + err.message, true);
    }
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
    adminPanelBtn.onclick = () => {
        showAdminLogin();
    };
    
    // Login button
    adminLoginBtn.onclick = () => {
        performAdminLogin();
    };
    
    // Close login button
    adminCloseBtn.onclick = () => {
        closeAdminLogin();
    };
    
    // Logout button
    adminLogoutBtn.onclick = () => {
        closeAdminDashboard();
    };
    
    // Enter key on username
    adminUsername.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performAdminLogin();
        }
    });
    
    // Enter key on password
    adminPassword.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performAdminLogin();
        }
    });
}
