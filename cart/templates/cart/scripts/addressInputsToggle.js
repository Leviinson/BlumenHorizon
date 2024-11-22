function addressInputsToggle() {
    const addressFields = [
        'country-container', 'city-container', 'postal-code-container',
        'street-container', 'building-number-container', 'apartment-container',
    ];
    
    addressFields.forEach(containerId => {
        const container = document.getElementById(containerId);
        const input = container.querySelector('input');

        if (this.checked) {
            container.style.display = 'none';
            ['country-container', 'city-container'].includes(containerId) ? '' : input.value = '';
            input.removeAttribute('required');
            container.querySelector('label').style.display = 'none';
        } else {
            container.style.display = 'block';
            input.setAttribute('required', '')
            container.querySelector('label').style.display = 'block';
        }
    });
}

document.getElementById('confirm-address').addEventListener('change', addressInputsToggle);