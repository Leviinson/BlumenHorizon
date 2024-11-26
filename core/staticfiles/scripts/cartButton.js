const updateCartButtonState = function (form, isInCart) {
    const button = form.querySelector("button");
    form.dataset.isInCart = isInCart ? "true" : "false";

    if (isInCart) {
        button.classList.replace("btn-dark-green", "btn-success");
    } else {
        button.classList.replace("btn-success", "btn-dark-green");
    }
};

const handleCartFormSubmit = async function (form) {
    const isInCart = form.dataset.isInCart === "true";
    const url = isInCart ? form.dataset.removeUrl : form.dataset.addUrl;

    form.setAttribute("action", url);

    try {
        const response = await fetch(url, {
            method: "POST",
            body: new FormData(form)
        });

        const data = await response.json();

        if (data.status === "success") {
            updateCartButtonState(form, !isInCart);
            showToast(data.detail, isInCart ? "danger" : "success");
        } else {
            showToast(data.detail, "danger");
        }
    } catch (error) {
        console.error(error);
        showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
    }
};

function addToCartListener(event) {
    event.preventDefault();
    handleCartFormSubmit(event.target);
}

document.addEventListener("DOMContentLoaded", function () {
    const cardsContainers = document.querySelectorAll(".cards-container");

    // Initialize buttons on other pages
    if (cardsContainers) {
        cardsContainers.forEach(cardsContainer => {
            cardsContainer.querySelectorAll(".add-to-cart-form").forEach(form => {
                updateCartButtonState(form, form.dataset.isInCart === "true");
                form.addEventListener("submit", addToCartListener)
            });
        })        
    }

    // Initialize button on product page
    const form = document.getElementById("add-to-cart-form");
    if (form) {
        updateCartButtonState(form, form.dataset.isInCart === "true");
        form.addEventListener("submit", addToCartListener);
    }
});
