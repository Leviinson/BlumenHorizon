function checkCardBodyContent() {
    const productsListContainer = document.getElementById("products-list-container");
    const noImageContainer = document.getElementById("no-image-container");
    const checkoutButton = document.getElementById("btn-checkout");
    console.log(document.querySelectorAll(".product-container"));
    if (productsListContainer && noImageContainer) {
        if (productsListContainer.querySelectorAll(".product-container").length === 0) {
            noImageContainer.classList.remove("d-none");
            noImageContainer.classList.add("d-flex");
            checkoutButton.classList.add("disabled");
        } else {
            noImageContainer.classList.toggle("d-flex");
            noImageContainer.classList.add("d-none");
            checkoutButton.classList.remove("disabled");
        }
    }
}
document.addEventListener("DOMContentLoaded", function () {
    checkCardBodyContent();
});
