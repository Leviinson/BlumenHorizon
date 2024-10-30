document.addEventListener("DOMContentLoaded", function () {
    const cartContainer = document.getElementById("cart-container");

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
                showToast(data.message, isInCart ? "danger" : "success");
            } else {
                showToast(data.message, "danger");
            }
        } catch (error) {
            console.error(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    };

    // Initialize buttons on catalog page
    if (cartContainer) {
        cartContainer.querySelectorAll(".add-to-cart-form").forEach(form => {
            updateButtonState(form, form.dataset.isInCart === "true");
        });

        cartContainer.addEventListener("submit", function (event) {
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

function showToast(message, type) {
    const toastContainer = document.getElementById("toast-container");

    const toastElement = document.createElement("div");
    toastElement.className = `toast align-items-center border-0`;
    toastElement.setAttribute("role", "alert");
    toastElement.setAttribute("aria-live", "assertive");
    toastElement.setAttribute("aria-atomic", "true");
    console.log(type);
    toastElement.innerHTML = `
        <div class="d-flex mt-2 text-bg-${type}">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastElement);

    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    toastElement.addEventListener("hidden.bs.toast", () => {
        toastElement.remove();
    });
}