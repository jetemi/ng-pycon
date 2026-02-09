/**
 * PyCon Nigeria 2024 Theme JavaScript
 * Theme-specific interactions and animations
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('PyCon Nigeria 2024 Theme loaded');
        
        // Animate elements on scroll
        initScrollAnimations();
        
        // Add interactive hover effects
        initInteractiveCards();
        
        // Initialize countdown if present
        initCountdown();
    });
    
    /**
     * Animate elements when they come into view
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe feature cards
        const cards = document.querySelectorAll('.theme-2024 .feature-card');
        cards.forEach(function(card) {
            observer.observe(card);
        });
    }
    
    /**
     * Add interactive effects to cards
     */
    function initInteractiveCards() {
        const cards = document.querySelectorAll('.theme-2024 .feature-card');
        
        cards.forEach(function(card) {
            card.addEventListener('mouseenter', function() {
                // Add a subtle scale effect
                this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }
    
    /**
     * Initialize countdown timer (if exists)
     */
    function initCountdown() {
        const countdownElement = document.querySelector('[x-data*="countdown"]');
        
        if (countdownElement) {
            console.log('Countdown timer detected for 2024 theme');
            // Countdown is handled by Alpine.js in the main template
            // This is just for theme-specific enhancements
        }
    }
    
    /**
     * Add parallax effect to hero section
     */
    function initParallax() {
        const hero = document.querySelector('.theme-2024 .hero-section');
        
        if (hero) {
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const parallax = scrolled * 0.5;
                hero.style.transform = 'translateY(' + parallax + 'px)';
            });
        }
    }
    
    // Export functions if needed
    window.Theme2024 = {
        initScrollAnimations: initScrollAnimations,
        initInteractiveCards: initInteractiveCards
    };
    
})();
