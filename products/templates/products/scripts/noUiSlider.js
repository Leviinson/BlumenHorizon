var slider = document.getElementById('priceSlider');
var minInput = document.getElementById('price__gte');
var maxInput = document.getElementById('price__lte');
var maxRange = parseInt(maxInput.getAttribute('max'));

noUiSlider.create(slider, {
    start: [minInput.value, maxInput.value],
    connect: true,
    range: {
        'min': 0,
        'max': maxRange
    },
    step: 0.1
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
