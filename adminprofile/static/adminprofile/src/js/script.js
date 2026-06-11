// get api token
document.getElementById('repo-btn').addEventListener('click', function () {
    window.location.href = "?sync=github";
});


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



