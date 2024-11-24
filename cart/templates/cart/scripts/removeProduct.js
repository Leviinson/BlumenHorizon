document.addEventListener("DOMContentLoaded", function () {
    const removeForms = document.querySelectorAll('.product-remove-form');

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
                const productElement = document.getElementById(productElementId);
                const grandTotalElement = document.getElementById("grand-total-price");
                const countElement = document.getElementById("total-count");
                const taxesElement = document.getElementById("taxes");

                document.getElementById('products-total-price').textContent = data.cartSubTotal;
                if (productElement) {
                    productElement.remove();
                    if (hr) {
                        hr.remove();
                    }
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
            console.log(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    }

    removeForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAjax(form);
        });
    });
});
