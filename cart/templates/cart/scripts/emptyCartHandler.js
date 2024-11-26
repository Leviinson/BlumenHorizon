function emptyCartHandler() {
    const productsListContainer = document.getElementById("products-list-container");
    const noImageContainer = document.getElementById("no-image-container");
    const checkoutButton = document.getElementById("btn-checkout");
    const cartClearButton = document.getElementById("cart-clear-button");
    const productCount = productsListContainer.querySelectorAll(".product-container").length;
    if (productsListContainer && noImageContainer) {
        if (productCount === 0) {
            noImageContainer.classList.remove("d-none");
            noImageContainer.classList.add("d-flex");
            checkoutButton.classList.add("disabled");
            cartClearButton.classList.add("disabled");
        } else {
            noImageContainer.classList.add("d-flex");
            noImageContainer.classList.remove("d-none");
            checkoutButton.classList.remove("disabled");
            cartClearButton.classList.remove("disabled");
        }
    }
}
document.addEventListener("DOMContentLoaded", function () {
    emptyCartHandler();
});
