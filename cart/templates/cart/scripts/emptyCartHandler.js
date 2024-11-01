function emptyCartHandler() {
    const productsListContainer = document.getElementById("products-list-container");
    const noImageContainer = document.getElementById("no-image-container");
    const checkoutButton = document.getElementById("btn-checkout");
    const cartClearButton = document.getElementById("cart-clear-button");
    const productCount = productsListContainer.querySelectorAll(".product-container").length;
    const expectedDeliveryTimeContainer = document.getElementById("expected-delivery-time");
    if (productsListContainer && noImageContainer) {
        if (productCount === 0) {
            noImageContainer.classList.remove("d-none");
            noImageContainer.classList.add("d-flex");
            checkoutButton.classList.add("disabled");
            cartClearButton.classList.add("disabled");
            expectedDeliveryTimeContainer.classList.add("d-none");
        } else {
            noImageContainer.classList.toggle("d-flex");
            noImageContainer.classList.add("d-none");
            checkoutButton.classList.remove("disabled");
            cartClearButton.classList.remove("disabled");
            expectedDeliveryTimeContainer.classList.remove("d-none");
        }
    }
}
document.addEventListener("DOMContentLoaded", function () {
    emptyCartHandler();
});
