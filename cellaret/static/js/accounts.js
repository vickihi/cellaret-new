document.addEventListener("DOMContentLoaded", function () {
    
    const toggleButton = document.querySelector(".js-inline-edit-toggle");
    const form = toggleButton ? toggleButton.closest("form") : null;

    if (!toggleButton || !form) return;

    const editableFields = form.querySelectorAll(
        'input[name="username"], input[name="email"]'
    );
    const hasErrors = form.querySelector(".form-error");
    let isEditing = false;

    function enableEditMode() {
        editableFields.forEach((field) => {
            field.removeAttribute("readonly");
        });

        toggleButton.textContent = "Save changes";
        toggleButton.classList.remove("btn-secondary");
        toggleButton.classList.add("btn-primary");

        isEditing = true;
    }

    function disableEditMode() {
        editableFields.forEach((field) => {
            field.setAttribute("readonly", "readonly");
        });

        toggleButton.textContent = "Change account details";
        toggleButton.classList.add("btn-secondary");
        toggleButton.classList.add("btn-primary");

        isEditing = false;
    }

    if (hasErrors) {
        enableEditMode();
    }

    toggleButton.addEventListener("click", function () {
        if (!isEditing) {
            enableEditMode();
            editableFields[0]?.focus();
            return;
        }

        form.requestSubmit();
    });
});