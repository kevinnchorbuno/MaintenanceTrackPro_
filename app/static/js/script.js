// Main JavaScript for MaintenanceTrackPro

document.addEventListener('DOMContentLoaded', function() {
    // Hide loading overlay if it exists
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
        loadingOverlay.classList.remove('fade-in');
    }

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Add fade-out to alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            alert.classList.add('fade-out');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        });
    }, 5000);
    
    // Show loading overlay for page transitions (but not for forms)
    document.addEventListener('click', function(e) {
        // Only for links that navigate to another page (not for forms, # links, js actions, etc)
        const target = e.target.closest('a');
        if (target && 
            target.getAttribute('href') && 
            !target.getAttribute('href').startsWith('#') &&
            !target.getAttribute('href').startsWith('javascript:') &&
            !target.hasAttribute('data-bs-toggle') &&
            !target.classList.contains('no-loader') &&
            !target.closest('form') && // Don't show loader for links inside forms
            target.target !== '_blank') {
            
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
                setTimeout(() => {
                    loadingOverlay.classList.add('fade-in');
                }, 10);
            }
        }
    });
    
    // Form validation styling
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Add shake animation to invalid fields
                form.querySelectorAll(':invalid').forEach(field => {
                    field.classList.add('shake');
                    setTimeout(() => {
                        field.classList.remove('shake');
                    }, 500);
                });
            } else {
                // Show loading overlay for valid form submissions
                const loadingOverlay = document.getElementById('loading-overlay');
                if (loadingOverlay) {
                    loadingOverlay.style.display = 'flex';
                    loadingOverlay.classList.add('fade-in');
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Notification counter update
    const notificationBadge = document.getElementById('notification-badge');
    if (notificationBadge) {
        setInterval(() => {
            fetch('/api/notifications/count')
                .then(response => response.json())
                .then(data => {
                    if (data.count > 0) {
                        notificationBadge.textContent = data.count;
                        notificationBadge.classList.remove('d-none');
                    } else {
                        notificationBadge.classList.add('d-none');
                    }
                })
                .catch(error => console.error('Error fetching notifications:', error));
        }, 60000); // Check every minute
    }
    
    // Update equipment health animation
    const healthBars = document.querySelectorAll('.health-bar');
    healthBars.forEach(bar => {
        const value = parseFloat(bar.style.width);
        // Add the appropriate class based on the health value
        if (value >= 70) {
            bar.classList.add('health-status-healthy');
        } else if (value >= 60) {
            bar.classList.add('health-status-warning');
        } else {
            bar.classList.add('health-status-critical');
        }
    });
    
    // Custom file input styling
    document.querySelectorAll('.custom-file-input').forEach(input => {
        input.addEventListener('change', (e) => {
            let fileName = e.target.files[0].name;
            let nextSibling = e.target.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });
}); 