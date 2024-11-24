document.addEventListener("DOMContentLoaded", function () {
    const decreaseForms = document.querySelectorAll('.product-decrease-form');
    const increaseForms = document.querySelectorAll('.product-increase-form');

    async function sendAjax(form) {
        const quantityInput = document.getElementById(form.dataset.productQuantityInputId);
        const subtotalElement = document.getElementById(form.dataset.subtotalId);
        const grandTotalElement = document.getElementById("grand-total-price");
        const countElement = document.getElementById("total-count");
        const taxesElement = document.getElementById("taxes");

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                quantityInput.value = data.productQuantity;
                countElement.textContent = interpolate(gettext('%s эл.'), [data.totalQuantity]);
                subtotalElement.textContent = data.productGrandTotal;
                grandTotalElement.textContent = data.cartGrandTotal;
                document.getElementById('products-total-price').textContent = data.cartSubTotal;
                taxesElement.textContent = data.taxes;
            } else {
                showToast(data.detail, "danger");
            }
        } catch (error) {
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    }

    decreaseForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const quantityInput = document.getElementById(form.dataset.productQuantityInputId);
            if (parseInt(quantityInput.value) <= 1) {
                e.preventDefault();
                showToast(gettext("В корзине всего один продукт. Вместо уменьшения количества - удалите его."), "danger");
            } else {
                e.preventDefault();
                sendAjax(form);
            }
        });
    });

    increaseForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAjax(form);
        });
    });
});
