// Doesn't show filters on mobiles automatically

const filtersButton = document.getElementById('filtersButton');
const card = document.getElementById('filtersCard');
const filterAccordion = document.getElementById('filterAccordion');

let flag = 0 // to check if button was clicked
function updateBorder() {
    const mediaQuery = window.matchMedia('(max-width: 767px)');

    if (mediaQuery.matches) {
        if (flag % 2 == 1 ) {
            card.style.border = '1px solid #ccc';
        } else {
            card.classList.add("show");
            card.style.border = 'none';
        }
        flag += 1
    } else {
        filterAccordion.classList.add("show");
    }
}
updateBorder();
filtersButton.addEventListener('click', updateBorder);
