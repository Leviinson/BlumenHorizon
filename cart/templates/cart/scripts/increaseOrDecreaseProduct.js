function initializeCartListeners(containerId = "products-list-container") {
    const productsListContainer = document.getElementById(containerId);

    async function sendAjax(form) {
        const quantityInput = document.querySelector(`[data-id='${form.dataset.productQuantityInputId}']`);
        const subtotalElement = document.querySelector(`[data-id='${form.dataset.subtotalId}']`);
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

    function handleDecreaseFormSubmit(e) {
        const form = e.target;
        const quantityInput = document.querySelector(`[data-id='${form.dataset.productQuantityInputId}']`);
        if (parseInt(quantityInput.value) <= 1) {
            e.preventDefault();
            showToast(gettext("В корзине всего один продукт. Вместо уменьшения количества - удалите его."), "danger");
        } else {
            e.preventDefault();
            sendAjax(form);
        }
    }

    function handleIncreaseFormSubmit(e) {
        e.preventDefault();
        sendAjax(e.target);
    }

    function attachFormEventListeners() {
        const decreaseForms = productsListContainer.querySelectorAll('.product-decrease-form');
        const increaseForms = productsListContainer.querySelectorAll('.product-increase-form');

        decreaseForms.forEach(form => {
            form.removeEventListener('submit', handleDecreaseFormSubmit);
            form.addEventListener('submit', handleDecreaseFormSubmit);
        });

        increaseForms.forEach(form => {
            form.removeEventListener('submit', handleIncreaseFormSubmit);
            form.addEventListener('submit', handleIncreaseFormSubmit);
        });
    }

    attachFormEventListeners();
}
initializeCartListeners();