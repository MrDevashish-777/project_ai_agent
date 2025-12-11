/**
 * Booking Modal Functionality
 * Handles booking form modal display and submission
 */

let pendingHotel = null;

/**
 * Open booking modal for a hotel
 * @param {object} hotel - Hotel object
 */
function openBookingModal(hotel) {
    const modal = document.getElementById('booking-modal');
    const bName = document.getElementById('b-name');
    const bPhone = document.getElementById('b-phone');
    const bDate = document.getElementById('b-date');
    const bNights = document.getElementById('b-nights');
    const bVisitors = document.getElementById('b-visitors');
    
    pendingHotel = hotel;
    document.getElementById('book-title').textContent = `Complete Booking: ${hotel.name}`;
    bDate.value = '';
    bName.value = '';
    bPhone.value = '';
    bNights.value = userPreferences.nights || 1;
    bVisitors.value = userPreferences.visitors || 1;
    modal.style.display = 'flex';
}

/**
 * Close booking modal
 */
function closeBookingModal() {
    const modal = document.getElementById('booking-modal');
    modal.style.display = 'none';
    pendingHotel = null;
}

/**
 * Perform the booking
 * @param {string} name - Customer name
 * @param {string} phone - Customer phone
 * @param {string} hotelId - Hotel ID
 * @param {string} checkinDate - Check-in date
 * @param {number} nights - Number of nights
 * @param {number} visitors - Number of visitors
 */
async function performBook(name, phone, hotelId, checkinDate, nights, visitors) {
    const payload = {
        name,
        phone,
        hotel_id: hotelId,
        checkin_date: checkinDate,
        nights,
        visitors,
        user_id: getUserId()
    };
    
    try {
        const res = await fetch(`${BASE}/book`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) {
            const text = await res.text();
            addMessage('❌ Booking failed: ' + text, 'bot');
            showNotification('Booking failed!', true);
            return;
        }
        
        const data = await res.json();
        addMessage(data.bill, 'bot');
        showPaymentModal(data);
        showNotification('Opening payment details...', false);
    } catch (err) {
        addMessage('❌ Booking error: ' + err.message, 'bot');
        showNotification('Booking error!', true);
    }
}

/**
 * Initialize booking modal event listeners
 */
function initBookingListeners() {
    const modal = document.getElementById('booking-modal');
    const bCancel = document.getElementById('b-cancel');
    const bConfirm = document.getElementById('b-confirm');
    const bName = document.getElementById('b-name');
    const bPhone = document.getElementById('b-phone');
    const bDate = document.getElementById('b-date');
    const bNights = document.getElementById('b-nights');
    const bVisitors = document.getElementById('b-visitors');
    
    bCancel.onclick = () => {
        closeBookingModal();
        addMessage('❌ Booking cancelled.', 'bot');
    };
    
    bConfirm.onclick = () => {
        const name = bName.value.trim();
        const phone = bPhone.value.trim();
        const date = bDate.value;
        const nights = parseInt(bNights.value || '1');
        const visitors = parseInt(bVisitors.value || '1');
        
        if (!name || !phone || !date || !nights || !visitors || !pendingHotel) {
            showNotification('❌ Please fill in all fields!', true);
            return;
        }
        
        userPreferences.nights = nights;
        userPreferences.visitors = visitors;
        closeBookingModal();
        addMessage(`🔄 Confirming your booking for ${pendingHotel.name}...`, 'bot');
        performBook(name, phone, pendingHotel.id, date, nights, visitors);
    };
}
