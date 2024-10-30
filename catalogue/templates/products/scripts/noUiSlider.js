function createSlider(sliderId, minInputId, maxInputId, step = 10) {
    var slider = document.getElementById(sliderId);
    var minInput = document.getElementById(minInputId);
    var maxInput = document.getElementById(maxInputId);
    var maxRange = parseInt(maxInput.getAttribute('max'));

    noUiSlider.create(slider, {
        start: [minInput.value, maxInput.value],
        connect: true,
        range: {
            'min': 0,
            'max': maxRange
        },
        step: step
    });

    slider.noUiSlider.on('update', function (values, handle) {
        if (handle === 0) {
            minInput.value = Math.round(values[0]);
        } else {
            maxInput.value = Math.round(values[1]);
        }
    });

    minInput.addEventListener('input', function () {
        slider.noUiSlider.set([this.value, null]);
    });

    maxInput.addEventListener('input', function () {
        slider.noUiSlider.set([null, this.value]);
    });
}

const sliders = [
    { sliderId: 'priceSlider', minInputId: 'min_price_input', maxInputId: 'max_price_input' },
    { sliderId: 'sizeSlider', minInputId: 'min_size_input', maxInputId: 'max_size_input' },
    { sliderId: 'amountOfFlowersSlider', minInputId: 'min_amount_of_flowers_input', maxInputId: 'max_amount_of_flowers_input' },
];

sliders.forEach(({ sliderId, minInputId, maxInputId }) => {
    if (document.getElementById(sliderId)) {
        createSlider(sliderId, minInputId, maxInputId);
    }
});