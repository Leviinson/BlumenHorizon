function disableForm(form) {
    Array.from(form.elements).forEach(element => element.disabled = true);
}