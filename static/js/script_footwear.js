const mainGrid = document.getElementById("mainProductGrid");
const searchGrid = document.getElementById("searchProductGrid");
const searchInput = document.getElementById("searchInput");

let Products = [];

fetch('/api/footwear')
  .then(res => res.json())
  .then(data => {
    Products = data.map((p, index) => ({
      ...p,
      id: `footwear_db-${p.id || index + 1}`,
      source: 'footwear_db'
    }));
    renderProducts(mainGrid, Products);
  })
  .catch(error => console.error("Failed to load products", error));

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

      const card = e.target.closest('.col-12');
      const productId = btn.getAttribute('data-product-id');
      const quantitySelect = card.querySelector('.quantity-select');
      const sizeSelect = card.querySelector('.size-select');
      const quantity = parseInt(quantitySelect?.value);
      const size = sizeSelect?.value;

      const product = Products.find(p => p.id === productId);

      if (!product) {
        console.error("Product not found for ID:", productId);
        alert("Product not found.");
        return;
      }

      if (!size) {
        alert("Please select a size.");
        return;
      }

      if (isNaN(quantity) || quantity <= 0) {
        alert("Please select a valid quantity.");
        return;
      }

      if (quantity > parseInt(product.stock)) {
        alert(`Only ${product.stock} in stock. Please choose a lower quantity.`);
        return;
      }


      if (typeof cart !== 'undefined' && cart.addItem) {
        cart.addItem(product, quantity, size);

        btn.textContent = 'Added!';
        btn.classList.add('btn-success');
        setTimeout(() => {
          btn.textContent = 'Add to Cart';
          btn.classList.remove('btn-success');
        }, 1000);

        if (quantitySelect) quantitySelect.value = '';
        if (sizeSelect) sizeSelect.value = '';
      } else {
        alert("Cart system not initialized.");
      }
    });
  });
}

function renderProducts(gridElement, products) {
  gridElement.innerHTML = "";

  products.forEach((product) => {
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
              <select class="form-select mb-2 mx-auto size-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
                <option selected value="">Size</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
              </select>
              <select class="form-select mb-3 mx-auto quantity-select" style="max-width: 200px;" ${isOutOfStock ? 'disabled' : ''}>
                <option selected value="">Quantity</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
              <button class="btn btn-dark mb-2 mx-auto py-2 add-to-cart" style="max-width: 200px;" data-product-id="${productId}" ${isOutOfStock ? 'disabled' : ''}>
                ${isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
              </button>
              <!-- Size Chart Button and Collapse for Footwear -->
              <button class="btn btn-dark text-white mb-2 p-2" style="max-width: 200px" type="button" data-bs-toggle="collapse" data-bs-target="#sizeChart-${productId}" aria-expanded="false" aria-controls="sizeChart-${productId}">
                Size Chart
              </button>
              <div class="collapse size-chart mt-2" id="sizeChart-${productId}">
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
