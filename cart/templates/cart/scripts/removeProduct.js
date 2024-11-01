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
                document.getElementById('products-total-price').textContent = data.grand_total;
                if (productElement) {
                    productElement.remove();
                    if (hr) {
                        hr.remove();
                    }
                    countElement.textContent = data.count;
                    grandTotalElement.textContent = data.grand_total;
                    emptyCartHandler();
                }
                showToast(data.message, "danger");
            } else {
                showToast(data.message, "danger");
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
