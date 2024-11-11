document.addEventListener("DOMContentLoaded", function () {
    const cardsContainer = document.getElementById("cards-container");

    const updateButtonState = function (form, isInCart) {
        const button = form.querySelector("button");
        form.dataset.isInCart = isInCart ? "true" : "false";

        if (isInCart) {
            button.classList.replace("btn-dark-green", "btn-success");
        } else {
            button.classList.replace("btn-success", "btn-dark-green");
        }
    };

    const handleCartFormSubmit = async function (form) {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const isInCart = form.dataset.isInCart === "true";
        const url = isInCart ? form.dataset.removeUrl : form.dataset.addUrl;

        form.setAttribute("action", url);

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                },
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                updateButtonState(form, !isInCart);
                showToast(data.detail, isInCart ? "danger" : "success");
            } else {
                showToast(data.detail, "danger");
            }
        } catch (error) {
            console.error(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    };

    // Initialize buttons on catalog page
    if (cardsContainer) {
        cardsContainer.querySelectorAll(".add-to-cart-form").forEach(form => {
            updateButtonState(form, form.dataset.isInCart === "true");
        });

        cardsContainer.addEventListener("submit", function (event) {
            if (event.target.matches(".add-to-cart-form")) {
                event.preventDefault();
                handleCartFormSubmit(event.target);
            }
        });
    }

    // Initialize button on product page
    const form = document.getElementById("add-to-cart-form");
    if (form) {
        updateButtonState(form, form.dataset.isInCart === "true");

        form.addEventListener("submit", function (event) {
            event.preventDefault();
            handleCartFormSubmit(form);
        });
    }
});
