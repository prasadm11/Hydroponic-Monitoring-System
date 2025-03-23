// Your UPI ID
const upiID = "pmmahajan2002@oksbi";  // Replace with your UPI ID

// Function to generate the UPI payment link
function generateUPILink(amount) {
    return `upi://pay?pa=${upiID}&pn=YourName&am=${amount}&cu=INR`;
}

// Function to generate QR code for predefined amounts
function generateQRCode(amount) {
    const qr = new QRious({
        element: document.getElementById('qr'),
        size: 200,
        value: generateUPILink(amount)
    });
}

// Function to handle custom QR code generation
function generateCustomQRCode() {
    const customAmount = document.getElementById('customAmount').value;
    if (customAmount && customAmount > 1000) {
        generateQRCode(customAmount);
    } else {
        alert("Cannot contain value less than 1000");
    }
}

// Attach click event to predefined amount buttons
document.querySelectorAll('.amount-btn').forEach(button => {
    button.addEventListener('click', function () {
        const amount = this.getAttribute('data-amount');
        generateQRCode(amount);
    });
});