// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scrolling for anchor links
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

    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero-section');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});


// Testimonials carousel functionality
function initTestimonialsCarousel() {
    const testimonials = document.querySelectorAll('.testimonial-card');
    const dotsContainer = document.querySelector('.testimonial-dots');
    let currentTestimonial = 0;

    // Create dots if container exists
    if (dotsContainer) {
        testimonials.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = `w-3 h-3 rounded-full mx-1 transition-all duration-300 ${
                index === 0 ? 'bg-elegant-purple' : 'bg-gray-300'
            }`;
            dot.addEventListener('click', () => showTestimonial(index));
            dotsContainer.appendChild(dot);
        });
    }

    function showTestimonial(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.classList.toggle('hidden', i !== index);
            testimonial.classList.toggle('fade-in-up', i === index);
        });

        // Update dots
        if (dotsContainer) {
            dotsContainer.querySelectorAll('button').forEach((dot, i) => {
                dot.className = `w-3 h-3 rounded-full mx-1 transition-all duration-300 ${
                    i === index ? 'bg-elegant-purple' : 'bg-gray-300'
                }`;
            });
        }

        currentTestimonial = index;
    }

    // Auto-rotate testimonials
    setInterval(() => {
        const nextTestimonial = (currentTestimonial + 1) % testimonials.length;
        showTestimonial(nextTestimonial);
    }, 5000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTestimonialsCarousel();
});