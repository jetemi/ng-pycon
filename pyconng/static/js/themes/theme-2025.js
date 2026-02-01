/**
 * PyCon Nigeria 2025 Theme JavaScript
 * Theme-specific interactions and animations
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('PyCon Nigeria 2025 Theme loaded');
        
        // Animate elements on scroll
        initScrollAnimations();
        
        // Add interactive effects
        initInteractiveEffects();
        
        // Add stagger animations
        initStaggerAnimations();
    });
    
    /**
     * Animate elements when they come into view
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-slide');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe all animatable elements
        const elements = document.querySelectorAll('.theme-2025 .feature-card, .theme-2025 .section-title');
        elements.forEach(function(element) {
            observer.observe(element);
        });
    }
    
    /**
     * Add interactive effects to cards
     */
    function initInteractiveEffects() {
        const cards = document.querySelectorAll('.theme-2025 .feature-card');
        
        cards.forEach(function(card) {
            // Add ripple effect on click
            card.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                ripple.style.left = e.clientX - card.offsetLeft + 'px';
                ripple.style.top = e.clientY - card.offsetTop + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(function() {
                    ripple.remove();
                }, 600);
            });
            
            // Enhanced hover effect
            card.addEventListener('mouseenter', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                this.style.setProperty('--mouse-x', x + 'px');
                this.style.setProperty('--mouse-y', y + 'px');
            });
        });
    }
    
    /**
     * Stagger animations for multiple elements
     */
    function initStaggerAnimations() {
        const groups = document.querySelectorAll('.theme-2025 .features-grid');
        
        groups.forEach(function(group) {
            const items = group.querySelectorAll('.feature-card');
            
            items.forEach(function(item, index) {
                // Add stagger delay
                item.style.animationDelay = (index * 0.1) + 's';
            });
        });
    }
    
    /**
     * Add smooth scroll behavior for links
     */
    function initSmoothScroll() {
        const links = document.querySelectorAll('.theme-2025 a[href^="#"]');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Export functions if needed
    window.Theme2025 = {
        initScrollAnimations: initScrollAnimations,
        initInteractiveEffects: initInteractiveEffects,
        initStaggerAnimations: initStaggerAnimations
    };
    
})();
