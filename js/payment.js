/**
 * Payment Modal Functionality
 * Handles payment modal display and payment processing
 */

let pendingBookingData = null;

/**
 * Show payment modal with booking details
 * @param {object} bookingData - Booking data from server
 */
async function showPaymentModal(bookingData) {
    const modal = document.getElementById('payment-modal');
    const subtotal = bookingData.total_price;
    const gst = subtotal * 0.18;
    const total = subtotal + gst;
    
    document.getElementById('p-hotel').textContent = bookingData.hotel.name;
    document.getElementById('p-subtotal').textContent = subtotal.toFixed(2);
    document.getElementById('p-gst').textContent = gst.toFixed(2);
    document.getElementById('p-total').textContent = total.toFixed(2);
    
    modal.style.display = 'flex';
}

/**
 * Close payment modal
 */
function closePaymentModal() {
    const modal = document.getElementById('payment-modal');
    modal.style.display = 'none';
    pendingBookingData = null;
}

/**
 * Proceed to payment processing
 * @param {object} bookingData - Booking data
 */
async function proceedToPayment(bookingData) {
    const subtotal = bookingData.total_price;
    const gst = subtotal * 0.18;
    const total = subtotal + gst;
    
    try {
        addMessage('💳 Creating payment intent...', 'bot');
        
        const paymentRes = await fetch(`${BASE}/internal/payment_intent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                amount_inr: Math.round(total),
                currency: 'INR',
                description: `Booking for ${bookingData.hotel.name}`,
                booking_id: bookingData.booking_id
            })
        });
        
        if (!paymentRes.ok) {
            throw new Error('Payment intent creation failed');
        }
        
        const paymentData = await paymentRes.json();
        document.getElementById('p-payment-link').href = paymentData.payment_url;
        document.getElementById('p-payment-url').style.display = 'block';
        
        addMessage('✅ Payment gateway ready! Click the payment link to complete payment.', 'bot');
        showNotification('Payment intent created. Click the payment link!', false);
        
        // Generate invoice after a short delay
        setTimeout(() => generateInvoice(bookingData.booking_id), 2000);
    } catch (err) {
        addMessage('❌ Payment error: ' + err.message, 'bot');
        showNotification('Payment setup failed!', true);
    }
}

/**
 * Generate invoice for booking
 * @param {string} bookingId - Booking ID
 */
async function generateInvoice(bookingId) {
    try {
        const invoiceRes = await fetch(`${BASE}/internal/generate_invoice`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                booking_id: bookingId,
                gst_percent: 18
            })
        });
        
        if (!invoiceRes.ok) {
            throw new Error('Invoice generation failed');
        }
        
        const invoiceData = await invoiceRes.json();
        addMessage(`📄 Invoice generated: ${invoiceData.invoice_id}`, 'bot');
        addMessage('✅ Booking complete! Check your email for invoice and payment details.', 'bot');
    } catch (err) {
        console.log('Note: Invoice generation skipped - ' + err.message);
    }
}

/**
 * Initialize payment modal event listeners
 */
function initPaymentListeners() {
    const pCancel = document.getElementById('p-cancel');
    const pConfirm = document.getElementById('p-confirm');
    
    pCancel.onclick = () => {
        closePaymentModal();
        addMessage('❌ Payment cancelled.', 'bot');
    };
    
    pConfirm.onclick = () => {
        if (pendingBookingData) {
            proceedToPayment(pendingBookingData);
        }
    };
}
