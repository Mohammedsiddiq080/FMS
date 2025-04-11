// Login Form
document.getElementById('loginForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'admin') {
        window.location.href = '/dashboard';
    } else {
        alert('Invalid username or password');
    }
});

// Auto-fill ID function (robust)
function autoFillID(module) {
    fetch(`/get_next_id/${module}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.next_id) {
                const idFieldMap = {
                    "drivers": "driver_id",
                    "fleet": "vehicle_id",
                    "billing": "record_id",
                    "assignments": "assignment_id",
                    "spares": "spare_id"
                };
                const fieldName = idFieldMap[module];
                const idInput = document.getElementById(fieldName);
                if (idInput) {
                    idInput.value = data.next_id;
                    idInput.readOnly = true;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching next ID:', error);
            generateLocalID(module);
        });
}

// Fallback local ID generation
function generateLocalID(module) {
    const prefixes = {
        "drivers": "DRV",
        "fleet": "VHL",
        "billing": "BL",
        "assignments": "ASN",
        "spares": "SPR"
    };
    const prefix = prefixes[module] || "";
    const randomNum = Math.floor(1000 + Math.random() * 9000);
    const id = `${prefix}${randomNum}`;

    const idFieldMap = {
        "drivers": "driver_id",
        "fleet": "vehicle_id",
        "billing": "record_id",
        "assignments": "assignment_id",
        "spares": "spare_id"
    };
    const fieldName = idFieldMap[module];
    const idInput = document.getElementById(fieldName);
    if (idInput) {
        idInput.value = id;
        idInput.readOnly = true;
    }
}

// Auto-fill IDs on page load and reset
window.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;

    if (path.includes("driver")) autoFillID("drivers");
    else if (path.includes("fleet")) autoFillID("fleet");
    else if (path.includes("billing")) autoFillID("billing");
    else if (path.includes("assignment")) autoFillID("assignments");
    else if (path.includes("spares")) autoFillID("spares");

    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('reset', () => {
            if (form.id === 'driverForm') autoFillID("drivers");
            else if (form.id === 'fleetForm') autoFillID("fleet");
            else if (form.id === 'billingForm') autoFillID("billing");
            else if (form.id === 'assignmentForm') autoFillID("assignments");
            else if (form.id === 'sparesForm') autoFillID("spares");
        });
    });
});

// Driver Form
document.getElementById('driverForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/driver', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        event.target.reset();
        autoFillID("drivers");
    })
    .catch(err => console.error('Error:', err));
});

// Fleet Form
document.getElementById('fleetForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/fleet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        event.target.reset();
        autoFillID("fleet");
    })
    .catch(err => console.error('Error:', err));
});

// Assignment Form
document.getElementById('assignmentForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/assignment', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        event.target.reset();
        autoFillID("assignments");
    })
    .catch(err => console.error('Error:', err));
});

// Billing Form
document.getElementById('billingForm')?.addEventListener('input', function() {
    calculateBilling();
});

document.getElementById('billingForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/billing', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        event.target.reset();
        autoFillID("billing");
    })
    .catch(err => console.error('Error:', err));
});

function calculateBilling() {
    const kmBefore = parseFloat(document.getElementById('km_before').value) || 0;
    const kmAfter = parseFloat(document.getElementById('km_after').value) || 0;
    const chargesPerKm = parseFloat(document.getElementById('charges_per_km').value) || 0;
    const gstRate = parseFloat(document.getElementById('gst').value) || 0;

    const distance = kmAfter - kmBefore;
    document.getElementById('distance').value = distance.toFixed(2);

    const subtotal = distance * chargesPerKm;
    document.getElementById('subtotal').value = subtotal.toFixed(2);

    const gstAmount = subtotal * (gstRate / 100);
    document.getElementById('gst_amount').value = gstAmount.toFixed(2);

    const totalAmount = subtotal + gstAmount;
    document.getElementById('total_amount').value = totalAmount.toFixed(2);
}

// Spares Form
document.getElementById('sparesForm')?.addEventListener('input', function() {
    calculateSpareCost();
});

document.getElementById('sparesForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/spares', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        event.target.reset();
        autoFillID("spares");
    })
    .catch(err => console.error('Error:', err));
});

function calculateSpareCost() {
    const unitPrice = parseFloat(document.getElementById('unit_price').value) || 0;
    const quantity = parseInt(document.getElementById('quantity').value) || 0;
    const totalCost = unitPrice * quantity;
    document.getElementById('total_cost').value = totalCost.toFixed(2);
}

// Fleet Maintenance Calculations
document.getElementById('fleetForm')?.addEventListener('input', function() {
    calculateMaintenance();
});

function calculateMaintenance() {
    const lastService = new Date(document.getElementById('last_service').value);
    const today = new Date();

    if (!isNaN(lastService.getTime())) {
        const daysSinceService = Math.floor((today - lastService) / (1000 * 60 * 60 * 24));
        // Display daysSinceService or use for maintenance logic
    }

    const mileage = parseFloat(document.getElementById('mileage').value) || 0;
    // Additional logic based on mileage
}
