document.addEventListener("DOMContentLoaded", function() {
    const addProductModal = document.getElementById("add-product-modal");
    const deleteProductModal = document.getElementById("delete-product-modal");
    const updateQuantityModal = document.getElementById("update-quantity-modal");
    const updatePriceModal = document.getElementById("update-price-modal"); // Add update price modal
    const showProductsModal = document.getElementById("show-products-modal");
    const messageModal = document.getElementById("message-modal"); // Error/Success Modal
    const messageText = document.getElementById("message-text"); // To display the message

    const addProductBtn = document.getElementById("add-product-btn");
    const deleteProductBtn = document.getElementById("delete-product-btn");
    const updateQuantityBtn = document.getElementById("update-quantity-btn");
    const updatePriceBtn = document.getElementById("update-price-btn"); // Add update price button
    const showProductsBtn = document.getElementById("show-products-btn");

    const closeAddModal = document.getElementById("close-add-modal");
    const closeDeleteModal = document.getElementById("close-delete-modal");
    const closeUpdateModal = document.getElementById("close-update-modal");
    const closeUpdatePriceModal = document.getElementById("close-update-price-modal"); // Close button for update price modal
    const closeShowModal = document.getElementById("close-show-modal");
    const closeMessageModal = document.getElementById("close-message-modal"); // Close button for error/success modal

    const submitAddProduct = document.getElementById("submit-add-product");
    const submitDeleteProduct = document.getElementById("submit-delete-product");
    const submitUpdateQuantity = document.getElementById("submit-update-quantity");
    const submitUpdatePrice = document.getElementById("submit-update-price"); // Add submit for update price

    const processing = document.getElementById("processing");

    addProductBtn.onclick = function() {
        addProductModal.style.display = "block";
    };

    deleteProductBtn.onclick = function() {
        deleteProductModal.style.display = "block";
    };

    updateQuantityBtn.onclick = function() {
        updateQuantityModal.style.display = "block";
    };

    updatePriceBtn.onclick = function() {  // Show update price modal
        updatePriceModal.style.display = "block";
    };

    showProductsBtn.onclick = function() {
        showProductsModal.style.display = "block";
        fetchProducts();
    };

    closeAddModal.onclick = function() {
        addProductModal.style.display = "none";
    };

    closeDeleteModal.onclick = function() {
        deleteProductModal.style.display = "none";
    };

    closeUpdateModal.onclick = function() {
        updateQuantityModal.style.display = "none";
    };

    closeUpdatePriceModal.onclick = function() {  // Close update price modal
        updatePriceModal.style.display = "none";
    };

    closeShowModal.onclick = function() {
        showProductsModal.style.display = "none";
    };

    closeMessageModal.onclick = function() {
        messageModal.style.display = "none";
    };

    function showProcessing() {
        processing.style.display = "block";
    }

    function hideProcessing() {
        processing.style.display = "none";
    }

    function showMessage(message) {
        messageText.innerText = message;
        messageModal.style.display = "block";
    }

    // Add Product
    submitAddProduct.onclick = function() {
        const product = document.getElementById("add-product-name").value;
        const price = document.getElementById("add-product-price").value;
        const quantity = document.getElementById("add-product-quantity").value;

        if (product && price && quantity) {
            showProcessing();
            fetch("/add_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ product, price, quantity })
            }).then(response => response.json())
            .then(data => {
                hideProcessing();
                if (data.status === 'error') {
                    showMessage(data.message);  // Show error message in modal
                } else {
                    showMessage(data.message);  // Show success message in modal
                }
                addProductModal.style.display = "none";
            });
        }
    };

    // Delete Product
    submitDeleteProduct.onclick = function() {
        const product = document.getElementById("delete-product-name").value;

        if (product) {
            showProcessing();
            fetch("/delete_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ product })
            }).then(response => response.json())
            .then(data => {
                hideProcessing();
                if (data.status === 'error') {
                    showMessage(data.message);  // Show error message in modal
                } else {
                    showMessage(data.message);  // Show success message in modal
                }
                deleteProductModal.style.display = "none";
            });
        }
    };

    // Update Quantity
    submitUpdateQuantity.onclick = function() {
        const product = document.getElementById("update-product-name").value;
        const quantity = document.getElementById("update-product-quantity").value;

        if (product && quantity) {
            showProcessing();
            fetch("/update_quantity", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ product, quantity })
            }).then(response => response.json())
            .then(data => {
                hideProcessing();
                if (data.status === 'error') {
                    showMessage(data.message);  // Show error message in modal
                } else {
                    showMessage(data.message);  // Show success message in modal
                }
                updateQuantityModal.style.display = "none";
            });
        }
    };

    // Update Price
    submitUpdatePrice.onclick = function() {
        const product = document.getElementById("update-product-name").value;
        const price = document.getElementById("update-product-price").value;

        if (product && price) {
            showProcessing();
            fetch("/update_price", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ product, price })
            }).then(response => response.json())
            .then(data => {
                hideProcessing();
                if (data.status === 'error') {
                    showMessage(data.message);  // Show error message in modal
                } else {
                    showMessage(data.message);  // Show success message in modal
                }
                updatePriceModal.style.display = "none";
            });
        }
    };

    // Fetch Products
    function fetchProducts() {
        fetch("/show_products")
        .then(response => response.json())
        .then(products => {
            const productList = document.getElementById("product-list");
            productList.innerHTML = "";
            products.forEach(product => {
                const li = document.createElement("li");
                li.textContent = `${product.product_name} - ${product.price} - Quantity: ${product.quantity}`;
                productList.appendChild(li);
            });
        });
    }
});
