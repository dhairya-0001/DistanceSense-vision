// Subtly animate dashboard elements over time
document.addEventListener("DOMContentLoaded", () => {
    const corners = document.querySelectorAll('.corner');
    
    // Pulse animation for corners
    setInterval(() => {
        corners.forEach(corner => {
            corner.style.opacity = Math.random() > 0.5 ? '1' : '0.5';
            corner.style.borderColor = Math.random() > 0.5 ? 'var(--accent-blue)' : 'var(--accent-green)';
        });
    }, 2000);
});
