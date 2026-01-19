// Animate elements on page load
document.addEventListener('DOMContentLoaded', function () {
    // Add entrance animations
    const card = document.querySelector('.card');
    if (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';

        setTimeout(() => {
            card.style.transition = 'all 0.8s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    }

    // Animate progress bar if it exists
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0%';

        setTimeout(() => {
            progressBar.style.width = targetWidth;
        }, 500);
    }

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add typing animation effect to input
    const inputField = document.querySelector('.input-field');
    if (inputField) {
        inputField.addEventListener('focus', function () {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.3s ease';
        });

        inputField.addEventListener('blur', function () {
            this.parentElement.style.transform = 'scale(1)';
        });
    }

    // Animate score value counting
    const scoreValue = document.querySelector('.score-value');
    if (scoreValue) {
        const targetScore = parseInt(scoreValue.textContent);
        let currentScore = 0;
        const increment = targetScore / 30; // 30 frames
        const duration = 1000; // 1 second
        const frameTime = duration / 30;

        scoreValue.textContent = '0';

        const counter = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(counter);
            }
            scoreValue.textContent = Math.floor(currentScore);
        }, frameTime);
    }

    // Add hover effect to reason items
    const reasonItems = document.querySelectorAll('.reason-item');
    reasonItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;

        item.addEventListener('mouseenter', function () {
            this.style.background = 'rgba(0, 102, 255, 0.1)';
        });

        item.addEventListener('mouseleave', function () {
            this.style.background = 'var(--bg-input)';
        });
    });

    // Add particle effect on form submit
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const submitBtn = this.querySelector('.btn-primary');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
                submitBtn.disabled = true;
            }
        });
    }

    // Add glowing effect to status card
    const statusCard = document.querySelector('.status-card');
    if (statusCard) {
        // Pulse animation
        setInterval(() => {
            statusCard.style.transition = 'box-shadow 1s ease-in-out';
            const currentShadow = window.getComputedStyle(statusCard).boxShadow;

            if (statusCard.classList.contains('status-malicious')) {
                statusCard.style.boxShadow = '0 0 40px rgba(255, 51, 102, 0.4)';
            } else if (statusCard.classList.contains('status-suspicious')) {
                statusCard.style.boxShadow = '0 0 40px rgba(255, 149, 0, 0.4)';
            } else if (statusCard.classList.contains('status-safe')) {
                statusCard.style.boxShadow = '0 0 40px rgba(0, 204, 102, 0.4)';
            }

            setTimeout(() => {
                if (statusCard.classList.contains('status-malicious')) {
                    statusCard.style.boxShadow = '0 0 30px rgba(255, 51, 102, 0.2)';
                } else if (statusCard.classList.contains('status-suspicious')) {
                    statusCard.style.boxShadow = '0 0 30px rgba(255, 149, 0, 0.2)';
                } else if (statusCard.classList.contains('status-safe')) {
                    statusCard.style.boxShadow = '0 0 30px rgba(0, 204, 102, 0.2)';
                }
            }, 500);
        }, 2000);
    }
});

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }
});

// Add floating particles effect
function createParticle() {
    const particle = document.createElement('div');
    particle.style.position = 'fixed';
    particle.style.width = '2px';
    particle.style.height = '2px';
    particle.style.background = 'rgba(0, 212, 255, 0.5)';
    particle.style.borderRadius = '50%';
    particle.style.pointerEvents = 'none';
    particle.style.left = Math.random() * window.innerWidth + 'px';
    particle.style.top = window.innerHeight + 'px';
    particle.style.zIndex = '0';

    document.body.appendChild(particle);

    const duration = 3000 + Math.random() * 2000;
    const drift = (Math.random() - 0.5) * 100;

    particle.animate([
        {
            transform: `translate(0, 0) scale(1)`,
            opacity: 0
        },
        {
            transform: `translate(${drift}px, -${window.innerHeight}px) scale(1.5)`,
            opacity: 0.8
        },
        {
            transform: `translate(${drift * 2}px, -${window.innerHeight * 2}px) scale(0.5)`,
            opacity: 0
        }
    ], {
        duration: duration,
        easing: 'ease-out'
    }).onfinish = () => particle.remove();
}

// Create particles periodically
setInterval(createParticle, 500);
