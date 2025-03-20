document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('dark-icon');
    const lightIcon = document.getElementById('light-icon');
    const htmlElement = document.documentElement;
    
    // Check for saved theme preference or use device preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        enableDarkMode();
    } else {
        enableLightMode();
    }
    
    // Toggle theme on button click
    themeToggle.addEventListener('click', function() {
        if (htmlElement.getAttribute('data-bs-theme') === 'dark') {
            enableLightMode();
        } else {
            enableDarkMode();
        }
    });
    
    // Function to enable dark mode
    function enableDarkMode() {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        darkIcon.classList.add('d-none');
        lightIcon.classList.remove('d-none');
        localStorage.setItem('theme', 'dark');
        
        // Add animation
        document.body.classList.add('theme-transition');
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 500);
    }
    
    // Function to enable light mode
    function enableLightMode() {
        htmlElement.setAttribute('data-bs-theme', 'light');
        lightIcon.classList.add('d-none');
        darkIcon.classList.remove('d-none');
        localStorage.setItem('theme', 'light');
        
        // Add animation
        document.body.classList.add('theme-transition');
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 500);
    }
}); 