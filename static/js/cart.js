const cart = {
  items: [],
  total: 0,

  // Helper function to get product stock from server
  async getProductStock(productId, source) {
    try {
      const response = await fetch(`/api/product_stock?id=${productId}&source=${source}`);
      const data = await response.json();
      return data.stock || 0;
    } catch (error) {
      console.error('Error fetching product stock:', error);
      return 0;
    }
  },

  addItem: async function (product, quantity = 1, size = "Medium") {
    // Get current stock for the product
    const currentStock = await this.getProductStock(product.id, product.source);
    
    const existingItem = this.items.find(
      (item) => item.id === product.id && item.size === size && item.source === product.source
    );

    let newQuantity = quantity;
    if (existingItem) {
      newQuantity = existingItem.quantity + quantity;
    }

    // Check if the new quantity exceeds available stock
    if (newQuantity > currentStock) {
      const availableToAdd = currentStock - (existingItem ? existingItem.quantity : 0);
      if (availableToAdd <= 0) {
        alert(`Sorry, "${product.name}" is out of stock!`);
        return;
      } else {
        alert(`Only ${availableToAdd} items available. Adding ${availableToAdd} to cart.`);
        newQuantity = currentStock;
        quantity = availableToAdd;
      }
    }

    if (existingItem) {
      existingItem.quantity = newQuantity;
    } else {
      this.items.push({
        id: product.id,
        name: product.name,
        price: parseFloat(product.price.replace("₱", "")),
        size: size,
        quantity: quantity,
        image: product.image,
        source: product.source,
        stock: currentStock // Store stock info
      });
    }

    this.calculateTotal();
    this.save();
    this.updateCartUI();
    renderFullCart(); // Ensure the main cart view is updated

    const toast = document.getElementById("addedToCartToast");
    if (toast) new bootstrap.Toast(toast).show();
  },

  removeItem: function (id, size, source) {
    this.items = this.items.filter(
      (item) => !(item.id === id && item.size === size && item.source === source)
    );
    this.calculateTotal();
    this.save();
    this.updateCartUI();
    renderFullCart(); // Re-render main cart after removal
  },

  // New method to update item quantity with stock validation
  updateItemQuantity: async function(id, size, source, newQuantity) {
    const item = this.items.find(i => i.id === id && i.size === size && i.source === source);
    if (!item) return;

    if (newQuantity <= 0) {
      this.removeItem(id, size, source);
      return;
    }

    // Get current stock for validation
    const currentStock = await this.getProductStock(id, source);
    
    if (newQuantity > currentStock) {
      alert(`Only ${currentStock} items available in stock.`);
      item.quantity = currentStock;
    } else {
      item.quantity = newQuantity;
    }

    this.calculateTotal();
    this.save();
    this.updateCartUI();
    renderFullCart(); // Re-render main cart after quantity update
  },

  calculateTotal: function () {
    this.total = this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  },

  updateCartUI: function () {
    const cartItemsEl = document.getElementById("cartItems");
    const cartCountEl = document.getElementById("cartCount");
    const cartTotalEl = document.getElementById("cartTotal");
    const checkoutBtn = document.getElementById("checkoutBtn"); // For dropdown checkout button

    if (cartCountEl) {
      cartCountEl.textContent = this.items.reduce((sum, item) => sum + item.quantity, 0);
    }

    if (cartItemsEl) {
      if (this.items.length === 0) {
        cartItemsEl.innerHTML = '<p class="text-muted mb-0">Your cart is empty</p>';
        if (checkoutBtn) checkoutBtn.disabled = true;
      } else {
        cartItemsEl.innerHTML = this.items
          .map((item) => `
            <div class="d-flex mb-2 border-bottom pb-2">
              <img src="${item.image}" width="50" height="50" class="me-2 rounded">
              <div class="flex-grow-1">
                <h6 class="mb-1">${item.name}</h6>
                <small class="text-muted">Size: ${item.size} | Qty: ${item.quantity}</small>
                ${item.stock !== undefined ? `<small class="text-info d-block">Stock: ${item.stock}</small>` : ''}
              </div>
              <div class="text-end">
                <h6 class="mb-1">₱${(item.price * item.quantity).toFixed(2)}</h6>
                <button class="btn btn-sm btn-outline-danger remove-item" 
                        data-id="${item.id}" 
                        data-size="${item.size}" 
                        data-source="${item.source}">
                  <i class="bi bi-trash"></i> 
                </button>
              </div>
            </div>
          `).join("");
        if (checkoutBtn) checkoutBtn.disabled = false;
      }
    }

    if (cartTotalEl) {
      cartTotalEl.textContent = `₱${this.total.toFixed(2)}`;
    }
  },

  save: function () {
    // Save cart to server session
    fetch('/api/cart', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: this.items })
    });
  },

  load: function () {
    // Load cart from server session
    fetch('/api/cart', {
        method: 'GET',
        credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
        this.items = data.items || [];
        this.calculateTotal();
        this.updateCartUI();
        renderFullCart(); // Call for the unified cart display
    });
  },

  clear: function () {
    this.items = [];
    this.total = 0;
    this.save();
    this.updateCartUI();
    renderFullCart(); // Re-render the unified cart after clear
  },
};

async function renderFullCart() {
  const fullCartContainer = document.getElementById("fullCartItems");
  const emptyCartMessage = document.getElementById("emptyCartMessage"); // Unified empty message
  const fullCartTotalEl = document.getElementById("fullCartTotal"); // Unified total amount display
  const proceedToCheckoutBtn = document.getElementById("proceedToCheckoutBtn");
  const clearCartBtn = document.getElementById("clearCartBtn");

  if (!fullCartContainer || !emptyCartMessage || !fullCartTotalEl) return;

  // Update stock information for all items
  for (let item of cart.items) {
    item.stock = await cart.getProductStock(item.id, item.source);
  }

  if (cart.items.length === 0) {
    fullCartContainer.innerHTML = '';
    emptyCartMessage.style.display = 'block'; // Show unified empty cart message
    fullCartTotalEl.textContent = `₱0.00`;
    if (proceedToCheckoutBtn) proceedToCheckoutBtn.disabled = true;
    if (clearCartBtn) clearCartBtn.disabled = true;
    return;
  }

  emptyCartMessage.style.display = 'none'; // Hide unified empty cart message

  fullCartContainer.innerHTML = cart.items.map((item) => `
    <div class="cart-item-card d-flex align-items-center mb-3">
        <img src="${item.image}" class="cart-item-image me-3" alt="${item.name}">
        <div class="cart-item-details">
            <h6 class="cart-item-name">${item.name}</h6>
            <div class="cart-item-meta">Size: ${item.size}</div>
            <div class="cart-item-meta text-info">Stock: ${item.stock}</div>
            ${item.quantity > item.stock ? '<div class="cart-item-meta text-danger">⚠️ Quantity exceeds stock!</div>' : ''}
            <div class="d-flex align-items-center justify-content-between mt-2">
                <div class="quantity-controls">
                    <button class="quantity-btn quantity-minus" 
                            data-id="${item.id}" 
                            data-size="${item.size}" 
                            data-source="${item.source}">−</button>
                    <span class="quantity-display">${item.quantity}</span>
                    <button class="quantity-btn quantity-plus" 
                            data-id="${item.id}" 
                            data-size="${item.size}" 
                            data-source="${item.source}"
                            ${item.quantity >= item.stock ? 'disabled' : ''}>+</button>
                </div>
                <div class="text-end">
                    <div class="cart-item-price">₱${(item.price * item.quantity).toFixed(2)}</div>
                    <button class="remove-item-btn remove-item mt-2" 
                            data-id="${item.id}" 
                            data-size="${item.size}" 
                            data-source="${item.source}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
  `).join("");

  fullCartTotalEl.textContent = `₱${cart.total.toFixed(2)}`;
  if (proceedToCheckoutBtn) proceedToCheckoutBtn.disabled = false;
  if (clearCartBtn) clearCartBtn.disabled = false;
}

// renderMobileCart is no longer needed for rendering items as renderFullCart now handles the unified display
// We keep a simplified version to manage the display of the mobile-specific title and container,
// although the main rendering is handled by renderFullCart.
function renderMobileCart() {
    const mobilePageTitle = document.querySelector(".mobile-page-title");
    const mobileCartContainer = document.querySelector(".mobile-cart-container");

    if (mobilePageTitle && mobileCartContainer) {
        // These elements are now hidden on desktop by media queries in cart.css
        // Their visibility is handled by CSS, not JS for content rendering.
        // This function primarily ensures the initial state or any mobile-specific
        // toggles (if any were present) are correctly managed.
    }
}


// Save cart to server
function saveCartToServer() {
    fetch('/api/cart', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: cart.items })
    });
}

// Load cart from server
function loadCartFromServer() {
    fetch('/api/cart', {
        method: 'GET',
        credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
        cart.items = data.items || [];
        cart.calculateTotal();
        cart.updateCartUI();
        renderFullCart(); // Call renderFullCart for the unified display
    });
}

// Event listeners for the unified buttons
document.getElementById("clearCartBtn")?.addEventListener("click", () => {
  cart.clear();
});

// The old mobileClearCartBtn is now consolidated into clearCartBtn,
// so this specific listener is no longer needed if IDs are unified in HTML.
// If you keep separate IDs for some reason, ensure this is mapped correctly.
// document.getElementById("mobileClearCartBtn")?.addEventListener("click", () => {
//     cart.clear();
// });

document.addEventListener("DOMContentLoaded", function () {
  cart.load();
});

window.addEventListener("storage", function (e) {
  if (e.key === "cartItems" || e.key === "cartTotal") {
    cart.load();
    renderFullCart(); // Ensure unified cart is updated
  }
});

document.getElementById('proceedToCheckoutBtn')?.addEventListener('click', function() {
    window.location.href = '/checkout';
});

document.getElementById('checkoutBtn')?.addEventListener('click', function() {
    if (!this.disabled) {
        window.location.href = '/checkout';
    }
});

// The old mobileCheckoutBtn is now consolidated into proceedToCheckoutBtn,
// so this specific listener is no longer needed if IDs are unified in HTML.
// If you keep separate IDs for some reason, ensure this is mapped correctly.
// document.getElementById('mobileCheckoutBtn')?.addEventListener('click', function() {
//     if (!this.disabled) {
//         window.location.href = '/checkout';
//     }
// });

document.addEventListener("click", function (e) {

  if (
    e.target.classList.contains("remove-item") ||
    e.target.closest(".remove-item")
  ) {
    const btn = e.target.closest(".remove-item");
    const id = btn.getAttribute("data-id");
    const size = btn.getAttribute("data-size");
    const source = btn.getAttribute("data-source");
    cart.removeItem(id, size, source);
  }

  if (e.target.classList.contains("quantity-minus")) {
    const id = e.target.getAttribute("data-id");
    const size = e.target.getAttribute("data-size");
    const source = e.target.getAttribute("data-source");
    const item = cart.items.find(i => i.id === id && i.size === size && i.source === source);
    if (item && item.quantity > 1) {
      cart.updateItemQuantity(id, size, source, item.quantity - 1);
    }
  }

  if (e.target.classList.contains("quantity-plus")) {
    const id = e.target.getAttribute("data-id");
    const size = e.target.getAttribute("data-size");
    const source = e.target.getAttribute("data-source");
    const item = cart.items.find(i => i.id === id && i.size === size && i.source === source);
    if (item) {
      cart.updateItemQuantity(id, size, source, item.quantity + 1);
    }
  }

  if (e.target.classList.contains("add-to-cart")) {
    const button = e.target;
    const productCard = button.closest(".col-12");
    const productId = parseInt(button.getAttribute("data-product-id"));

    let product = null;

    if (typeof Products !== "undefined") {
      product = Products.find((p) => p.id === productId);
      product.source = "all_product";
    } else if (typeof TomProducts !== "undefined") {
      product = TomProducts.find((p) => p.id === productId);
      product.source = "tom_db";
    }

    const sizeSelect = productCard.querySelector(".size-select");
    const quantitySelect = productCard.querySelector(".quantity-select");

    const size = sizeSelect.value;
    const quantity = parseInt(quantitySelect.value);

    if (!size) {
      alert("Please select a size");
      return;
    }

    if (!quantity) {
      alert("Please select quantity");
      return;
    }

    // Use the updated addItem method which includes stock validation
    cart.addItem(product, quantity, size);

    // When building the cart item in JS:
    fetch('/add_to_cart', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        name: product.name,
        size: size,
        quantity: parseInt(quantity),
        price: product.price,
        image: product.image // or image_url
      })
    })

    sizeSelect.value = "";
    quantitySelect.value = "";
  }

});