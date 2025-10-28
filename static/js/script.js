const mainGrid = document.getElementById("mainProductGrid");
const searchGrid = document.getElementById("searchProductGrid");
const searchInput = document.getElementById("searchInput");
const searchResultsSection = document.getElementById("searchResultsSection");

let AllProducts = []; // This will now hold ALL products from all categories

// Function to fetch data from a specific API endpoint
async function fetchProducts(apiEndpoint, sourceName) {
  try {
    const res = await fetch(apiEndpoint);
    let data = await res.json();
    // IMPORTANT CHANGE: Create a globally unique 'id' by combining sourceName and original product.id
    // Handle cases where product.id might be undefined or null
    data = data.map((p, index) => {
      const originalId = p.id !== undefined && p.id !== null ? p.id : index;
      return {
        ...p,
        originalId: p.id,
        id: `${sourceName}-${originalId}`, // Composite ID for uniqueness across sources
        source: sourceName // Add the source field
      };
    });
    return data;
  } catch (error) {
    console.error(`Failed to load products from ${apiEndpoint}:`, error);
    return []; // Return an empty array on error
  }
}

// Fetch all products from all categories
async function loadAllProducts() {
  try {
    const [accessories, tom, footwear, tshirt, stickers] = await Promise.all([
      fetchProducts('/api/accessories', 'accessories_db'),
      fetchProducts('/api/tom', 'tom_db'),
      fetchProducts('/api/footwear', 'footwear_db'),
      fetchProducts('/api/tshirt', 'tshirt_db'),
      fetchProducts('/api/stickers', 'stickers_db')
    ]);

    AllProducts = [
      ...tshirt, // T-shirts first
      ...footwear, // Then footwear
      ...accessories, // Then accessories
      ...tom, // Then Tom Clutch
      ...stickers // Finally stickers
    ];

    // Debug: Log all products to check for ID conflicts
    console.log("All products loaded:", AllProducts);
    console.log("Product IDs:", AllProducts.map(p => ({ id: p.id, name: p.name, source: p.source })));

    // Check for duplicate IDs (should not happen with composite IDs)
    const ids = AllProducts.map(p => p.id);
    const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
    if (duplicateIds.length > 0) {
      console.error("Duplicate IDs found:", duplicateIds);
    }

    // Initial render of all products in the main grid
    renderProducts(mainGrid, AllProducts);
  } catch (error) {
    console.error("Error loading all products:", error);
  }
}

// Load products when the script runs
loadAllProducts();

// Search on input
// Search on input
searchInput.addEventListener("input", () => {
  const term = searchInput.value.toLowerCase().trim();

  if (term === "") {
    searchGrid.innerHTML = "";
    return;
  }

  const filtered = AllProducts.filter(
    p => p.name.toLowerCase().includes(term) || p.price.toLowerCase().includes(term)
  );

  renderProducts(searchGrid, filtered); // Show results only in search grid
});

function setupAddToCartButtons(gridElement) {
  const addToCartButtons = gridElement.querySelectorAll('.add-to-cart');
  addToCartButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      e.preventDefault();

      const card = btn.closest('.col-12');
      const productId = btn.getAttribute("data-product-id"); // This will be the composite ID

      // Debug: Log the product ID we're looking for
      console.log("Looking for product with ID:", productId);

      // Find the product in AllProducts using its composite ID
      const product = AllProducts.find(p => p.id === productId);

      if (!product) {
        console.error("Product not found:", productId);
        console.log("Available products:", AllProducts.map(p => ({ id: p.id, name: p.name, source: p.source })));
        return;
      }

      // Debug: Log the product we found
      console.log("Found product:", product);

      const sizeSelect = card.querySelector('.size-select');
      const quantitySelect = card.querySelector('.quantity-select');

      // --- IMPORTANT CHANGE START ---
      // Get the raw values first
      const selectedSize = sizeSelect ? sizeSelect.value : "";
      const selectedQuantity = quantitySelect ? parseInt(quantitySelect.value) : NaN; // Use NaN for invalid quantity
      // --- IMPORTANT CHANGE END ---

      // Adjusted validation for size and quantity
      // Now, validate the raw selected values
      if (product.source !== 'stickers_db' && (selectedSize === "" || selectedSize === "Size")) { // "Size" is the default option value
        alert("Please select a size.");
        // Optional: Add visual feedback here (e.g., sizeSelect.classList.add('is-invalid');)
        return;
      }
      if (isNaN(selectedQuantity) || selectedQuantity <= 0 || selectedQuantity === "") { // "" is the default quantity option
        alert("Please select a valid quantity.");
        // Optional: Add visual feedback here (e.g., quantitySelect.classList.add('is-invalid');)
        return;
      }

      // *** START OF NEWLY ADDED CODE ***
      // Check if requested quantity exceeds available stock
      if (selectedQuantity > parseInt(product.stock)) {
        alert(`Only ${product.stock} in stock. Please choose a lower quantity.`);
        return;
      }
      // *** END OF NEWLY ADDED CODE ***

      // If validation passes, use the selected values
      const size = selectedSize;
      const quantity = selectedQuantity;

      // Debug: Log what we're adding to cart
      console.log("Adding to cart:", {
        productId: product.id,
        name: product.name,
        size: size,
        quantity: quantity,
        source: product.source
      });

      // Use the cart object from cart.js
      if (typeof cart !== 'undefined') {
        // Pass the entire product object which now contains 'id' and 'source'
        cart.addItem(product, quantity, size);
        console.log("Successfully added to cart");
      } else {
        console.error("Cart object not found. Make sure cart.js is loaded before script.js.");
      }

      // Reset form fields
      // Ensure dropdowns reset to their default "empty" options
      if (sizeSelect && sizeSelect.tagName === 'SELECT') sizeSelect.value = "";
      if (quantitySelect) quantitySelect.value = "";
    });
  });
}

// Reusable rendering with scroll on card click
function renderProducts(gridElement, products) {
  gridElement.innerHTML = "";

  if (products.length === 0) {
    gridElement.innerHTML = '<p class="text-center col-12">No products found.</p>';
    return;
  }

  products.forEach((product, idx) => {
    const productId = product.id;
    const collapseId = `collapse-${gridElement.id}-${productId.replace(/[^a-zA-Z0-9]/g, '_')}-${idx}`;

    const isOutOfStock = !product.stock || parseInt(product.stock) <= 0;

    // Determine if size selection is needed for this product type
    // This now excludes 'accessories_db' along with 'stickers_db'
    const requiresSize = product.source !== 'stickers_db' && product.source !== 'accessories_db';

    let sizeOptionsHtml = '';
    if (requiresSize) {
      if (product.source === 'footwear_db') {
        sizeOptionsHtml = `
          <select class="form-select mb-2 mx-auto size-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
            <option selected value="">Size</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
          </select>
        `;
      } else { // Default sizes for T-shirts and Tom Clutch
        sizeOptionsHtml = `
          <select class="form-select mb-2 mx-auto size-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
            <option selected value="">Size</option>
            <option value="Small">Small</option>
            <option value="Medium">Medium</option>
            <option value="Large">Large</option>
          </select>
        `;
      }
    } else {
      // For stickers and accessories (or products without sizes), use a hidden input for "One Size"
      sizeOptionsHtml = `<input type="hidden" class="size-select" value="One Size">`;
    }

    const cardHtml = `
      <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4 d-flex flex-column align-items-center">
        <div class="card m-3 p-2 border-0 custom-card"
             style="width: 18rem; cursor: pointer;"
             data-bs-toggle="collapse"
             data-bs-target="#${collapseId}"
             aria-expanded="false"
             aria-controls="${collapseId}">
          <img src="${product.image}" class="card-img-top" alt="${product.alt || product.name}">
          <div class="card-body">
            <h6 class="card-text text-center">${product.name}</h6>
          </div>
        </div>
        <div class="collapse w-100" id="${collapseId}">
          <div class="card card-body p-3 bg-light rounded mt-2">
            <div class="text-center">
              <img src="${product.image}" class="img-fluid mb-3" alt="${product.alt || product.name}">
              <h5 class="card-title"><strong>${product.name}</strong></h5>
              <h6 class="card-text">${product.price}</h6>
              <div class="mb-2">
                <span class="badge ${isOutOfStock ? 'bg-danger' : 'bg-success'}">
                  ${isOutOfStock ? 'Out of stock' : 'In stock: ' + product.stock}
                </span>
              </div>
              ${sizeOptionsHtml}
              <select class="form-select mb-3 mx-auto quantity-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
                <option selected value="">Quantity</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
              <button class="btn btn-dark mb-2 mx-auto p-2 add-to-cart" style="max-width: 200px;" data-product-id="${productId}" ${isOutOfStock ? 'disabled' : ''}>
                ${isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
              </button>
              ${product.source === 'tshirt_db' ? `
                <button class="btn btn-dark text-white mb-2 p-2" style="max-width: 200px" type="button" data-bs-toggle="collapse" data-bs-target="#sizeChart${idx}" aria-expanded="false" aria-controls="sizeChart${idx}">
                  Size Chart
                </button>
                <div class="collapse size-chart mt-2" id="sizeChart${idx}">
                  <div class="d-flex justify-content-center">
                    <table class="table table-bordered table-sm align-middle mb-0 mx-auto" style="max-width: 350px;">
                      <thead class="table-light">
                        <tr>
                          <th>Measurement</th>
                          <th>Small</th>
                          <th>Medium</th>
                          <th>Large</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Chest Width (inches)</td>
                          <td>18</td>
                          <td>20</td>
                          <td>22</td>
                        </tr>
                        <tr>
                          <td>Body Length (inches)</td>
                          <td>27</td>
                          <td>28</td>
                          <td>29</td>
                        </tr>
                        <tr>
                          <td>Shoulder Width (inches)</td>
                          <td>16.5</td>
                          <td>17.5</td>
                          <td>18.5</td>
                        </tr>
                        <tr>
                          <td>Sleeve Length (inches)</td>
                          <td>7.5</td>
                          <td>8</td>
                          <td>8.5</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <small class="text-muted d-block text-center">*All measurements are in inches. Actual product measurements may vary by up to 0.5".</small>
                </div>
              ` : product.source === 'footwear_db' ? `
                <button class="btn btn-dark text-white mb-2 p-2" style="max-width: 200px" type="button" data-bs-toggle="collapse" data-bs-target="#sizeChart${idx}" aria-expanded="false" aria-controls="sizeChart${idx}">
                  Size Chart
                </button>
                <div class="collapse size-chart mt-2" id="sizeChart${idx}">
                  <div class="d-flex justify-content-center">
                    <table class="table table-bordered table-sm align-middle mb-0 mx-auto" style="max-width: 350px;">
                      <thead class="table-light">
                        <tr>
                          <th>Footwear Size</th>
                          <th>US 7</th>
                          <th>US 8</th>
                          <th>US 9</th>
                          <th>US 10</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Foot Length (cm)</td>
                          <td>25</td>
                          <td>26</td>
                          <td>27</td>
                          <td>28</td>
                        </tr>
                        <tr>
                          <td>EU Size</td>
                          <td>40</td>
                          <td>41</td>
                          <td>42</td>
                          <td>43</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <small class="text-muted d-block text-center">*Sizing may vary by style. Please refer to the product description for details.</small>
                </div>
              ` : ''}
            </div>
          </div>
        </div>
      </div>`;

    gridElement.insertAdjacentHTML('beforeend', cardHtml);
  });

  // Add scroll behavior after rendering
  const cards = gridElement.querySelectorAll('.custom-card');
  cards.forEach(card => {
    card.addEventListener('click', function () {
      const targetId = card.getAttribute('data-bs-target');
      if (!targetId) return;

      const collapseElement = document.querySelector(targetId);

      collapseElement.addEventListener('shown.bs.collapse', function handleScroll() {
        collapseElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        collapseElement.removeEventListener('shown.bs.collapse', handleScroll);
      });
    });
  });

  // Setup add-to-cart buttons after rendering
  setupAddToCartButtons(gridElement);
}