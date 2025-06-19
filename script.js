document.addEventListener('DOMContentLoaded', () => {
    const toggleForms = document.querySelectorAll('.toggle-form');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    // Toggle between login and signup forms
    toggleForms.forEach(toggle => {
        toggle.addEventListener('click', () => {
            document.querySelector('.form-box.login').classList.toggle('hidden');
            document.querySelector('.form-box.signup').classList.toggle('hidden');
        });
    });

    // Handle login form submission
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your login logic here
        window.location.href = 'home.html';
    });

    // Handle signup form submission
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your signup logic here
        window.location.href = 'home.html';
    });
});