// ── Theme Toggle ──
const themeBtn = document.getElementById('themeBtn');
const body = document.body;

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

// restore saved theme on load
if (localStorage.getItem('portfolio-theme') === 'light') {
    body.setAttribute('data-theme', 'light');
}

// ── Burger / Mobile Nav ──
const burgerBtn = document.getElementById('burgerBtn');
const mobileNav = document.querySelector('.modern-nav');

burgerBtn.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
});

// ── Tab switching ──
const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.dataset.tab;
        document.getElementById(target).classList.add('active');
    });
});
