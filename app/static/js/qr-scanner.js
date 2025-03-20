document.addEventListener('DOMContentLoaded', function () {
    // Check if scanner element exists on the page
    const scannerContainer = document.getElementById('qr-scanner');
    if (!scannerContainer) return;

    // Initialize QR scanner when button is clicked
    document.getElementById('start-scanner').addEventListener('click', function() {
        // Show scanner UI
        document.getElementById('scanner-ui').classList.remove('d-none');
        
        // Initialize scanner
        const scanner = new Instascan.Scanner({ 
            video: document.getElementById('scanner-preview'),
            mirror: false,
            backgroundScan: false
        });

        // Handle found QR codes
        scanner.addListener('scan', function (content) {
            // Play success sound
            const successSound = new Audio('/static/sounds/beep.mp3');
            successSound.play();
            
            // Show success message
            const resultDiv = document.getElementById('scan-result');
            resultDiv.innerHTML = `<div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>QR Code detected!
                <hr>
                <p>Redirecting to: ${content}</p>
            </div>`;
            
            // Add animation and redirect after delay
            scannerContainer.classList.add('fade-out');
            setTimeout(() => {
                window.location.href = content;
            }, 1500);
        });

        // Start camera
        Instascan.Camera.getCameras().then(function (cameras) {
            if (cameras.length > 0) {
                // Try to use environment camera on mobile (back camera) if available
                let selectedCamera = cameras[0];
                for(let camera of cameras) {
                    if(camera.name && camera.name.toLowerCase().includes('back')) {
                        selectedCamera = camera;
                        break;
                    }
                }
                scanner.start(selectedCamera);
            } else {
                console.error('No cameras found.');
                document.getElementById('scanner-ui').innerHTML = 
                    '<div class="alert alert-danger">No camera available on this device</div>';
            }
        }).catch(function (e) {
            console.error(e);
            document.getElementById('scanner-ui').innerHTML = 
                `<div class="alert alert-danger">Camera error: ${e.message}</div>`;
        });

        // Add stop scanner button functionality
        document.getElementById('stop-scanner').addEventListener('click', function() {
            scanner.stop();
            document.getElementById('scanner-ui').classList.add('d-none');
        });
    });
}); 