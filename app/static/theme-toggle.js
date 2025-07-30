const savedTheme = localStorage.getItem('theme');
if (savedTheme === "auto") {
    applySystemTheme();
} else if (savedTheme) {
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    document.querySelectorAll('[data-bs-theme-value]').forEach(function (btn) {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
        btn.querySelector('.ms-auto').classList.add('d-none');
        if (btn.getAttribute('data-bs-theme-value') === savedTheme) {
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
            btn.querySelector('.ms-auto').classList.remove('d-none');
        }
    });
} else {
    applySystemTheme();
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applySystemTheme);

document.querySelectorAll('[data-bs-theme-value]').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var theme = btn.getAttribute('data-bs-theme-value');
        if (theme === 'auto') {
            localStorage.setItem('theme', 'auto'); // <-- Save 'auto'
            applySystemTheme();
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
            localStorage.setItem('theme', theme);
        }
        // Update active state and checkmark visibility
        document.querySelectorAll('[data-bs-theme-value]').forEach(function (b) {
            b.classList.remove('active');
            b.setAttribute('aria-pressed', 'false');
            b.querySelector('.ms-auto').classList.add('d-none');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        btn.querySelector('.ms-auto').classList.remove('d-none');
    });
});

// Toggle search form visibility
document.getElementById("search-icon").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("search-form").classList.toggle("d-none");
    document.querySelector("#search-form input").focus();
});