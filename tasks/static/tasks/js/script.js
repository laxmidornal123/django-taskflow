document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide Django alerts
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const closeButton =
                alert.querySelector(".btn-close");

            if (closeButton) {
                closeButton.click();
            }

        }, 4000);

    });


    // Confirm delete actions
    const deleteButtons =
        document.querySelectorAll("[data-delete-confirm]");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this task?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});
