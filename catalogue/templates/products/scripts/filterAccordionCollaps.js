// Doesn't show filters on mobiles automatically

const filtersButton = document.getElementById('filtersButton');
const card = document.getElementById('filtersCard');

let flag = 0 // to check if button was clicked
function updateBorder() {
    if (flag % 2 == 0 ) {
        card.style.border = '1px solid #ccc';
    } else {
        card.style.border = 'none';
    }
    flag += 1
}
updateBorder();
filtersButton.addEventListener('click', updateBorder);
