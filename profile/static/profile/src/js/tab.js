document.addEventListener("DOMContentLoaded", function () {

    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get("tab");

    if (tab) {
        const target = document.querySelector(`[data-tab="${tab}"]`);
        if (target) {
            target.click();
        }
    }

});
