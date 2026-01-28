
document.addEventListener("DOMContentLoaded", function () {

    // --- 1. Preloader ---
    const preloader = document.getElementById('preloader');
    if (preloader) {
        // Check if preloader has already been shown in this session
        if (sessionStorage.getItem("preloaderSeen")) {
            // Already seen, hide immediately (no animation)
            preloader.style.display = 'none';
        } else {
            // First visit, show animation and set flag
            setTimeout(() => {
                preloader.classList.add('fade-out');
                // Remove from DOM after transition to prevent blocking
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 500);
            }, 3500); // Increased time to 3.5s per user request
            sessionStorage.setItem("preloaderSeen", "true");
        }
    }

    // --- 2. 3D Tilt Effect (Only on desktops/cards) ---
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Calculate center
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Calculate rotation (max 10 degrees)
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;

            // Apply transformation to the image inside
            const img = card.querySelector('img');
            if (img) {
                // Add a specific class to image if not present to enable specific styling
                img.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
                img.style.transition = 'none'; // Remove transition for instant follow
            }
        });

        card.addEventListener('mouseleave', () => {
            const img = card.querySelector('img');
            if (img) {
                img.style.transform = `perspective(1000px) rotateX(0) rotateY(0) scale(1)`;
                img.style.transition = 'transform 0.5s ease'; // Smooth return
            }
        });
    });

});
