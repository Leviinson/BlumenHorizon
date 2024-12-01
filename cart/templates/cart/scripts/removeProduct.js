function initializeRemoveForms(formSelector = '.product-remove-form') {
    const removeForms = document.querySelectorAll(formSelector);

    async function sendAjax(form) {
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                const hr = document.getElementById(form.dataset.hrId);
                const productElementId = form.dataset.productElementId;
                const productElement = document.querySelector(`[data-id='${productElementId}']`);
                const grandTotalElement = document.getElementById("grand-total-price");
                const countElement = document.getElementById("total-count");
                const taxesElement = document.getElementById("taxes");

                document.getElementById('products-total-price').textContent = data.cartSubTotal;
                if (productElement) {
                    productElement.remove();
                    if (hr) {
                        hr.remove();
                    }
                    const recommendedProductAddToCartForm = document.querySelector(`[data-id='${productElementId}AddForm']`);
                    updateCartButtonState(recommendedProductAddToCartForm, false);
                    countElement.textContent = interpolate(gettext('%s эл.'), [data.totalQuantity]);
                    taxesElement.textContent = data.taxes;
                    grandTotalElement.textContent = data.cartGrandTotal;
                    emptyCartHandler();
                }
                showToast(data.detail, "danger");
            } else {
                showToast(data.detail, "danger");
            }
        } catch (error) {
            console.error(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    }

    removeForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAjax(form);
        });
    });
}

initializeRemoveForms();
