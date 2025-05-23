document.addEventListener("DOMContentLoaded", function () {
    const cartClearForm = document.getElementById('cart-clear-form');

    async function sendAjax(form) {
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                const productsListContainer = document.getElementById("products-list-container");
                const grandTotalElement = document.getElementById("grand-total-price");
                const countElement = document.getElementById("total-count");
                const productsTotalPrice = document.getElementById('products-total-price');
                const productContainers = productsListContainer.querySelectorAll(".product-container")
                const hrElements = productsListContainer.querySelectorAll("hr");
                const taxesElement = document.getElementById("taxes");

                if (productsListContainer && grandTotalElement && countElement) {
                    countElement.textContent = interpolate(gettext('%s эл.'), [data.count]);
                    grandTotalElement.textContent = data.grand_total;
                    productsTotalPrice.textContent = data.grand_total;
                    taxesElement.textContent = data.grand_total;
                    productContainers.forEach(container => container.remove());
                    hrElements.forEach(hr => hr.remove());
                    const addToCartForms = document.querySelectorAll(".add-to-cart-form");
                    addToCartForms.forEach(form => {
                        updateCartButtonState(form, false);
                    });
                    emptyCartHandler();
                }
                showToast(data.detail, "danger");
            } else {
                showToast(data.detail, "danger");
            }
        } catch (error) {
            console.log(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    }

    cartClearForm.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAjax(cartClearForm);
        });
    });
