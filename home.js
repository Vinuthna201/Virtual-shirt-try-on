document.addEventListener('DOMContentLoaded', () => {
    // Function to launch demo
    const launchDemo = () => {
        fetch('/launch-demo', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => console.log('Demo launched:', data))
        .catch(error => console.error('Error:', error));
    };

    // Handle both demo buttons
    document.getElementById('tryDemo').addEventListener('click', launchDemo);
    document.getElementById('startTryOn').addEventListener('click', launchDemo);

    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const section = document.querySelector(this.getAttribute('href'));
                section.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});