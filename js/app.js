/**
 * Main Application Initialization
 * Initializes all functionality when the page loads
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all listeners and functionality
    initChatListeners();
    initBookingListeners();
    initPaymentListeners();
    initAdminListeners();
    initUIListeners();
    
    // Send initial greeting
    sendChat('Hi');
    
    // Set minimum date for check-in to today
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.min = today;
    });
});

/**
 * Initialize UI interaction listeners
 */
function initUIListeners() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Navbar background change on scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .hotel-card, .testimonial-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
    
    // Add click handler for chat icon
    document.getElementById('chatbot-icon').addEventListener('click', openChat);
    
    // Add click handlers for modal overlays (close on outside click)
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

/**
 * Open chat window
 */
function openChat() {
    const chatWindow = document.getElementById('chat-window');
    const chatIcon = document.getElementById('chatbot-icon');
    
    chatWindow.style.display = 'flex';
    chatIcon.style.display = 'none';
    
    // Add entrance animation
    chatWindow.style.animation = 'slideInRight 0.3s ease-out';
    
    // Focus on input
    setTimeout(() => {
        document.getElementById('chat-input').focus();
    }, 300);
}

/**
 * Close chat window
 */
function closeChat() {
    const chatWindow = document.getElementById('chat-window');
    const chatIcon = document.getElementById('chatbot-icon');
    
    // Add exit animation
    chatWindow.style.animation = 'slideOutRight 0.3s ease-out';
    
    setTimeout(() => {
        chatWindow.style.display = 'none';
        chatIcon.style.display = 'flex';
    }, 300);
}

/**
 * Send suggestion message
 */
function sendSuggestion(message) {
    const chatInput = document.getElementById('chat-input');
    chatInput.value = message;
    
    // Add visual feedback
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    suggestionChips.forEach(chip => {
        if (chip.textContent.includes(message.split(' ')[0])) {
            chip.style.background = 'var(--primary-color)';
            chip.style.color = 'var(--white)';
            setTimeout(() => {
                chip.style.background = '';
                chip.style.color = '';
            }, 1000);
        }
    });
    
    document.getElementById('send-btn').click();
}

/**
 * Close booking modal
 */
function closeBookingModal() {
    const modal = document.getElementById('booking-modal');
    modal.style.animation = 'fadeOut 0.3s ease-out';
    setTimeout(() => {
        modal.style.display = 'none';
        modal.style.animation = '';
    }, 300);
}

/**
 * Close payment modal
 */
function closePaymentModal() {
    const modal = document.getElementById('payment-modal');
    modal.style.animation = 'fadeOut 0.3s ease-out';
    setTimeout(() => {
        modal.style.display = 'none';
        modal.style.animation = '';
    }, 300);
}

/**
 * Close admin modal
 */
function closeAdminModal() {
    const modal = document.getElementById('admin-login-modal');
    modal.style.animation = 'fadeOut 0.3s ease-out';
    setTimeout(() => {
        modal.style.display = 'none';
        modal.style.animation = '';
    }, 300);
}

/**
 * Show notification
 */
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = type === 'error' ? 'error' : '';
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.classList.add('hide');
        setTimeout(() => {
            notification.style.display = 'none';
            notification.classList.remove('hide');
        }, 300);
    }, 3000);
}

/**
 * Add typing indicator
 */
function showTypingIndicator() {
    const chatBody = document.getElementById('chat-body');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'msg bot typing';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<i class="fas fa-circle"></i> <i class="fas fa-circle"></i> <i class="fas fa-circle"></i> AI is typing...';
    chatBody.appendChild(typingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

/**
 * Remove typing indicator
 */
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
