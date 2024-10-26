// Doesn't show filters on mobiles automatically

const filterAccordion = document.getElementById('filterAccordion');

function toggleFilterAccordion() {
    const mediaQuery = window.matchMedia('(min-width: 767px)');

    if (mediaQuery.matches) {
        filterAccordion.classList.add('show');
    } else {
        filterAccordion.classList.remove('show');
    }
}
toggleFilterAccordion();
window.addEventListener('resize', toggleFilterAccordion);

const filtersButton = document.getElementById('filtersButton');
const card = document.getElementById('filtersCard');

let flag = 0 // to check if button was clicked
function updateBorder() {
    if (window.matchMedia('(max-width: 767px)').matches ) {
        if (flag % 2 == 1 ) {
            card.style.border = '1px solid #ccc';
        } else {
            card.style.border = 'none';
        }
        flag += 1
    }
}
updateBorder();
filtersButton.addEventListener('click', updateBorder);


function toggleFilterBorder() {
    const mediaQuery = window.matchMedia('(min-width: 767px)');

    if (mediaQuery.matches) {
        card.style.border = '1px solid #ccc';
    } else {
        card.style.border = 'none';
    }
}
toggleFilterBorder();

window.addEventListener('resize', toggleFilterBorder);