document.addEventListener('DOMContentLoaded', function() {
    var dateInput = document.getElementById('delivery-date');
    var timeInput = document.getElementById('delivery-time');

    var today = new Date();
    today.setHours(today.getHours() + 3);
    var day = today.getDate().toString().padStart(2, '0');
    var month = (today.getMonth() + 1).toString().padStart(2, '0');
    var year = today.getFullYear();
    var dateStr = `${year}-${month}-${day}`;
    dateInput.setAttribute('min', dateStr);
    dateInput.setAttribute('value', dateStr);

    function setMinTime() {
      var selectedDate = new Date(dateInput.value);
      
      if (selectedDate.toDateString() === today.toDateString()) {
        var hours = today.getHours().toString().padStart(2, '0');
        var minutes = today.getMinutes().toString().padStart(2, '0');
        var timeStr = `${hours}:${minutes}`;
        timeInput.setAttribute('min', timeStr);
        timeInput.setAttribute('value', timeStr);
      } else {
        timeInput.removeAttribute('min');
      }
    }

    dateInput.addEventListener('change', setMinTime);
    setMinTime();
  });