const mainGrid = document.getElementById("mainProductGrid");
const searchGrid = document.getElementById("searchProductGrid");
const searchInput = document.getElementById("searchInput");

let Products = [];

// Fetch from API
fetch('/api/stickers')
  .then(res => res.json())
  .then(data => {
    Products = data.map((p, index) => ({
      ...p,
      id: `stickers_db-${p.id || index + 1}`,
      source: 'stickers_db'
    }));
    renderProducts(mainGrid, Products);
  })
  .catch(error => console.error("Failed to load products", error));

// Search on input
searchInput.addEventListener("input", () => {
  const term = searchInput.value.toLowerCase().trim();
  if (term === "") {
    searchGrid.innerHTML = "";
    return;
  }
  const filtered = Products.filter(
    p => p.name.toLowerCase().includes(term) || p.price.toLowerCase().includes(term)
  );
  renderProducts(searchGrid, filtered);
});

function setupAddToCartButtons(gridElement) {
  const addToCartButtons = gridElement.querySelectorAll('.add-to-cart');
  addToCartButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      e.preventDefault();

      const card = btn.closest('.col-12');
      const productId = btn.getAttribute("data-product-id");
      const product = Products.find(p => p.id === productId);

      const quantitySelect = card.querySelector('.quantity-select');
      const quantity = parseInt(quantitySelect.value);
      const size = "One Size"; // Stickers don't have size selection

      if (isNaN(quantity) || quantity <= 0) {
        alert("Please select a valid quantity.");
        return;
      }

      if (!product) {
        console.error("Product not found:", productId);
        alert("Product not found.");
        return;
      }

      if (quantity > parseInt(product.stock)) {
        alert(`Only ${product.stock} in stock. Please choose a lower quantity.`);
        return;
      }


      if (typeof cart !== 'undefined') {
        cart.addItem(product, quantity, size);
      } else {
        alert("Cart system is not initialized.");
      }

      quantitySelect.value = "";
    });
  });
}

function renderProducts(gridElement, products) {
  gridElement.innerHTML = "";

  products.forEach(product => {
    const productId = product.id;
    const collapseId = `collapse-${gridElement.id}-${productId}`;
    const isOutOfStock = !product.stock || parseInt(product.stock) <= 0;

    const cardHtml = `
      <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4 d-flex flex-column align-items-center">
        <div class="card m-3 p-2 border-0 custom-card"
              style="width: 18rem; cursor: pointer;"
              data-bs-toggle="collapse" 
              data-bs-target="#${collapseId}" 
              aria-expanded="false" 
              aria-controls="${collapseId}">
          <img src="${product.image}" class="card-img-top" alt="${product.alt}">
          <div class="card-body">
            <h6 class="card-text text-center">${product.name}</h6>
          </div>
        </div>
        <div class="collapse w-100" id="${collapseId}">
          <div class="card card-body p-3 bg-light rounded mt-2">
            <div class="text-center">
              <img src="${product.image}" class="img-fluid mb-3" alt="${product.alt}">
              <h5 class="card-title"><strong>${product.name}</strong></h5>
              <h6 class="card-text">${product.price}</h6>
              <div class="mb-2">
                <span class="badge ${isOutOfStock ? 'bg-danger' : 'bg-success'}">
                  ${isOutOfStock ? 'Out of stock' : 'In stock: ' + product.stock}
                </span>
              </div>
              <input type="hidden" class="size-select" value="One Size">
              <select class="form-select mb-3 mx-auto quantity-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
                <option selected value="">Quantity</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
              <button class="btn btn-dark mb-2 mx-auto py-2 add-to-cart" style="max-width: 200px;" data-product-id="${productId}" ${isOutOfStock ? 'disabled' : ''}>
                ${isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
              </button>
            </div>
          </div>
        </div>
      </div>`;

    gridElement.insertAdjacentHTML('beforeend', cardHtml);
  });

  const cards = gridElement.querySelectorAll('.custom-card');
  cards.forEach(card => {
    card.addEventListener('click', function () {
      const targetId = card.getAttribute('data-bs-target');
      const collapseElement = document.querySelector(targetId);
      if (!collapseElement) return;

      collapseElement.addEventListener('shown.bs.collapse', function handleScroll() {
        collapseElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        collapseElement.removeEventListener('shown.bs.collapse', handleScroll);
      });
    });
  });

  setupAddToCartButtons(gridElement);
}
