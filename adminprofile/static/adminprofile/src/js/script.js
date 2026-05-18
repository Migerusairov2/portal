document.getElementById('repo-btn').addEventListener('click', function () {
    window.location.href = "?sync=github";
});
const themeBtn = document.getElementById('themeBtn');
const body = document.body;

// Toggle Theme
themeBtn.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');

    if (currentTheme === 'light') {
        body.removeAttribute('data-theme');
        localStorage.setItem('portfolio-theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        localStorage.setItem('portfolio-theme', 'light');
    }
});

if (localStorage.getItem('portfolio-theme') === 'light') {
    body.setAttribute('data-theme', 'light');
}

const tabs = document.querySelectorAll(".tab");
const contents = document.querySelectorAll(".tab-content");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {

        // remove active from all tabs
        tabs.forEach(t => t.classList.remove("active"));

        // hide all content
        contents.forEach(c => c.classList.remove("active"));

        // activate clicked tab
        tab.classList.add("active");

        // show matching content
        const target = tab.dataset.tab;
        document.getElementById(target).classList.add("active");
    });
});

const burgerBtn = document.getElementById("burgerBtn");
const mobileNav = document.querySelector(".modern-nav");

burgerBtn.addEventListener("click", () => {
    mobileNav.classList.toggle("active");

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