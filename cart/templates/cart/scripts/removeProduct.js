document.addEventListener("DOMContentLoaded", function () {
    const removeForms = document.querySelectorAll('.product-remove-form');

    async function sendAjax(form) {
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
                body: new URLSearchParams(new FormData(form))
            });

            const data = await response.json();

            if (data.status === "success") {
                const hr = document.getElementById(form.dataset.hrId);
                const productElementId = form.dataset.productElementId;
                const productElement = document.getElementById(productElementId);
                const grandTotalElement = document.getElementById("grand-total-price");
                if (productElement) {
                    productElement.remove();
                    hr.remove();
                    grandTotalElement.textContent = data.grand_total;
                }
            } else {
                showToast(data.message, "danger");
            }
        } catch (error) {
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
