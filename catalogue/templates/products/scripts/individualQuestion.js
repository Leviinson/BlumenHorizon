document.addEventListener("DOMContentLoaded", function () {
    const individualQuestionForm = document.getElementById('individual-question-form');

    async function sendAjax(form) {
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            const data = await response.json();

            if (data.status === "success") {
                showToast(data.message, "success");
                disableForm(form);
            } else {
                let errors = JSON.parse(data.errors);
                let errorsText = Object.entries(errors)
                    .map(([field, errors]) => {
                        return errors.map(error => `${error.message}`).join('\n');
                    })
                    .join('\n');

                showToast(`${data.message}\n${errorsText}`, "danger");
            }
        } catch (error) {
            console.log(error);
            showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
        }
    }



    individualQuestionForm.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAjax(individualQuestionForm);
        });
    });