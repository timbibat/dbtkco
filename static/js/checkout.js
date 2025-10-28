document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("checkoutItems");
  const totalEl = document.getElementById("checkoutTotal");
  const checkoutForm = document.getElementById("checkoutForm");

  if (!container || !totalEl || !checkoutForm) {
    console.error("Checkout elements not found in the DOM.");
    return;
  }

  // Define a local cart object if not already defined
  const checkoutCart = {
    items: [],
    total: 0,
    calculateTotal: function () {
      this.total = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }
  };

  function renderCheckoutItems() {
    if (checkoutCart.items.length === 0) {
      container.innerHTML = '<div class="alert alert-warning">Your checkout cart is empty.</div>';
      totalEl.textContent = "₱0.00";
      checkoutForm.style.display = "none";
      return;
    }

    container.innerHTML = checkoutCart.items.map((item) => `
      <div class="checkout-item mb-3 d-flex align-items-start gap-3 border-bottom pb-3">
        <img src="${item.image || 'placeholder.jpg'}" width="80" class="rounded">
        <div>
          <strong>${item.name}</strong><br>
          Size: ${item.size} | Qty: ${item.quantity}<br>
          Price: ₱${(item.price * item.quantity).toFixed(2)}
        </div>
      </div>
    `).join("");

    totalEl.textContent = `₱${checkoutCart.total.toFixed(2)}`;
  }

  // Load cart from server before rendering
  fetch('/api/cart', {
    method: 'GET',
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      checkoutCart.items = data.items || [];
      checkoutCart.calculateTotal();
      renderCheckoutItems();
    });

  checkoutForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const province = document.getElementById("province")?.value.trim();
    const municipality = document.getElementById("municipality")?.value.trim();
    const barangay = document.getElementById("barangay")?.value.trim();
    const zipcode = document.getElementById("zipcode")?.value.trim();
    const houseNumber = document.getElementById("houseNumber")?.value.trim();
    const landmark = document.getElementById("landmark")?.value.trim();
    const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked')?.value?.trim();
    const codPhone = document.getElementById("codPhone")?.value.trim();

    // Card fields
    const cardNumber = document.getElementById("cardNumber")?.value.replace(/\s+/g, '');
    const cardExpiry = document.getElementById("cardExpiry")?.value.trim();
    const cardCVC = document.getElementById("cardCVC")?.value.trim();

    // Build full address
    const address = `${houseNumber}, ${barangay}, ${municipality}, ${province}, ${zipcode}`;

    // Validate required fields
    if (!name || !email || !province || !municipality || !barangay || !zipcode || !houseNumber || !paymentMethod) {
      alert("Please complete all fields.");
      return;
    }

    // Validate phone number for COD
    if (paymentMethod === "Cash on Delivery") {
      if (!/^09\d{9}$/.test(codPhone)) {
        alert("Please enter a valid Philippine phone number (11 digits, starts with 09).");
        document.getElementById("codPhone").focus();
        return;
      }
    }

    // Validate card details for Debit/Credit Card
    if (paymentMethod === "Debit/Credit Card") {
      // Card number: 16 digits
      if (!/^\d{16}$/.test(cardNumber)) {
        alert("Please enter a valid 16-digit card number.");
        document.getElementById("cardNumber").focus();
        return;
      }
      // Expiry: MM/YY, not expired
      if (!/^\d{2}\/\d{2}$/.test(cardExpiry)) {
        alert("Please enter a valid expiry date (MM/YY).");
        document.getElementById("cardExpiry").focus();
        return;
      } else {
        const [mm, yy] = cardExpiry.split('/').map(Number);
        const now = new Date();
        const currentYear = now.getFullYear() % 100;
        const currentMonth = now.getMonth() + 1;
        if (mm < 1 || mm > 12 || yy < currentYear || (yy === currentYear && mm < currentMonth)) {
          alert("Please enter a valid expiry date (MM/YY) that is not expired.");
          document.getElementById("cardExpiry").focus();
          return;
        }
      }
      // CVC: 3 or 4 digits
      if (!/^\d{3,4}$/.test(cardCVC)) {
        alert("Please enter a valid 3 or 4 digit CVC.");
        document.getElementById("cardCVC").focus();
        return;
      }
    }

    // Get cart items and total (adjust if your cart is stored differently)
    const payload = {
      name,
      email,
      address,
      landmark,
      province,
      municipality,
      barangay,
      paymentMethod,
      codPhone,
      items: checkoutCart.items,
      total: checkoutCart.total
    };

    // Submit order via fetch
    const response = await fetch('/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (result.status === "success") {
      window.location.href = result.redirect;
    } else {
      alert(result.message || "There was an error placing your order.");
    }
  });
});