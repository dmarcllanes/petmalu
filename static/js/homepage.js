// ==================== Auth Interceptor ====================
// If Supabase redirects here because of missing Redirect URL configuration
// in the Dashboard, forward the token to the login page for processing
if (window.location.hash && window.location.hash.includes('access_token=')) {
    window.location.href = '/login' + window.location.hash;
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            const target = document.querySelector(href);
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add active state to nav links based on scroll position
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Button click handlers for CTA buttons
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    button.addEventListener('click', function () {
        const buttonText = this.textContent;
        console.log('CTA clicked:', buttonText);
        // Here you would typically navigate to a signup/login page
        // window.location.href = '/signup';
    });
});

// Fade-in animation on scroll for elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for fade-in effect
document.querySelectorAll('.feature-card, .pricing-card, .step, .problem-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// Add hover effect to cards
document.querySelectorAll('.feature-card, .pricing-card, .problem-item').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.cursor = 'pointer';
    });
});

// Navbar scroll effect
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 100) {
        navbar.style.boxShadow = '0 4px 12px rgba(47, 122, 115, 0.1)';
    } else {
        navbar.style.boxShadow = '0 1px 0 rgba(0, 0, 0, 0.05)';
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Add input validation for potential form (future enhancement)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Analytics tracking (optional - can be connected to your analytics service)
function trackEvent(eventName, eventData = {}) {
    console.log('Event tracked:', eventName, eventData);
    // Send to analytics service here
}

// Track CTA clicks
document.querySelectorAll('.btn-primary, .btn-secondary, .btn-outline').forEach(button => {
    button.addEventListener('click', function () {
        trackEvent('button_click', {
            buttonText: this.textContent,
            timestamp: new Date().toISOString()
        });
    });
});

// Debounce function for resize events
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Handle responsive behavior
const handleResize = debounce(() => {
    if (window.innerWidth <= 768) {
        // Mobile adjustments if needed
    }
}, 250);

window.addEventListener('resize', handleResize);

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    console.log('PetNourish landing page loaded');
    // Add any initialization code here
});
