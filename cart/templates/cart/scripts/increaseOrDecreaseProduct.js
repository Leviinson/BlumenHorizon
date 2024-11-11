document.addEventListener("DOMContentLoaded", function () {
    const decreaseForms = document.querySelectorAll('.product-decrease-form');
    const increaseForms = document.querySelectorAll('.product-increase-form');

    async function sendAjax(form) {
        const quantityInput = document.getElementById(form.dataset.productQuantityInputId);
        const subtotalElement = document.getElementById(form.dataset.subtotalId);
        const grandTotalElement = document.getElementById("grand-total-price");
        const countElement = document.getElementById("total-count");

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                quantityInput.value = data.quantity;
                subtotalElement.textContent = data.subtotal;
                grandTotalElement.textContent = data.grand_total;
                countElement.textContent = interpolate(gettext('%s эл.'), [data.count]);
                document.getElementById('products-total-price').textContent = data.grand_total;
            } else {
                showToast(data.message, "danger");
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
