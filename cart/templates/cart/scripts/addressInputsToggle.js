document.getElementById('confirm-address').addEventListener('change', function() {
    const addressFields = [
        'country-container', 'city-container', 'postal-code-container',
        'street-container', 'building-number-container', 'apartment-container',
        'recipient-name-container', 'recipient-phone-container'
    ];
    
    addressFields.forEach(containerId => {
        const container = document.getElementById(containerId);
        const input = container.querySelector('input');

        if (this.checked) {
            // Скрываем контейнер и очищаем его значение
            container.style.display = 'none';
            input.value = '';
            container.querySelector('label').style.display = 'none'; // Скрываем label
        } else {
            // Показываем контейнер
            container.style.display = 'block';
            container.querySelector('label').style.display = 'block'; // Показываем label
        }
    });
});