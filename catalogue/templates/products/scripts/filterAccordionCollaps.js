const filtersButton = document.getElementById('filtersButton');
const card = document.getElementById('filtersCard');
const filterAccordion = document.getElementById('filterAccordion');

let flag = 0;

function updateFilters() {
    const mediaQuery = window.matchMedia('(max-width: 767px)');
    if (mediaQuery.matches) {
        if (flag % 2 === 1) {
            card.style.border = '1px solid #ccc';
            filterAccordion.classList.add("show");
            flag += 1;
        } else {
            card.style.border = 'none';
            filterAccordion.classList.remove("show");
        }
    } else {
        card.style.border = '1px solid #ccc';
        filterAccordion.classList.add("show");
    }
}
updateFilters();
filtersButton.addEventListener('click', updateFilters);
window.addEventListener('resize', updateFilters);
