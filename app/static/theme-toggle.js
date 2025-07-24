function applySystemTheme() {
    var autoBtn = document.querySelector('[data-bs-theme-value="auto"]');
    if (autoBtn && autoBtn.classList.contains('active')) {
        var systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-bs-theme', systemPrefersDark ? 'dark' : 'light');
    }
}

// Initial theme detection
applySystemTheme();

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applySystemTheme);

document.querySelectorAll('[data-bs-theme-value]').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var theme = btn.getAttribute('data-bs-theme-value');
        if (theme === 'auto') {
            applySystemTheme();
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
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