// script.js
document.querySelectorAll('.login-btn').forEach(button => {
    button.addEventListener('click', () => {
        alert('Login as ' + button.textContent.trim());
    });
});
