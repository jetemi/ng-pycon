/**
 * PyCon Nigeria 2026 Theme JavaScript
 * Theme-specific interactions and animations
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('PyCon Nigeria 2026 Theme loaded');
        
        // Initialize all theme features
        initScrollAnimations();
        initInteractiveCards();
        initYearBadge();
        initSmoothScroll();
    });
    
    /**
     * Animate elements when they scroll into view
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -80px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Add stagger effect for grid items
                    if (entry.target.parentElement.classList.contains('features-grid')) {
                        const siblings = Array.from(entry.target.parentElement.children);
                        const index = siblings.indexOf(entry.target);
                        entry.target.style.animationDelay = (index * 0.1) + 's';
                    }
                    
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe elements
        const elements = document.querySelectorAll(
            '.theme-2026 .feature-card, ' +
            '.theme-2026 .section-title, ' +
            '.theme-2026 .sponsor-card'
        );
        
        elements.forEach(function(element) {
            observer.observe(element);
        });
    }
    
    /**
     * Add interactive effects to cards
     */
    function initInteractiveCards() {
        const cards = document.querySelectorAll('.theme-2026 .feature-card');
        
        cards.forEach(function(card) {
            // Track mouse position for subtle tilt effect
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const deltaX = (x - centerX) / centerX;
                const deltaY = (y - centerY) / centerY;
                
                // Subtle tilt effect
                this.style.transform = 
                    'perspective(1000px) ' +
                    'rotateY(' + (deltaX * 2) + 'deg) ' +
                    'rotateX(' + (-deltaY * 2) + 'deg) ' +
                    'translateY(-8px)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }
    
    /**
     * Enhance year badge with interactions
     */
    function initYearBadge() {
        const badge = document.querySelector('.theme-2026 .year-badge');
        
        if (badge) {
            // Add pulse effect on hover
            badge.addEventListener('mouseenter', function() {
                this.classList.add('pulse-on-hover');
            });
            
            badge.addEventListener('mouseleave', function() {
                this.classList.remove('pulse-on-hover');
            });
            
            // Optional: Make it clickable to scroll to top
            badge.addEventListener('click', function() {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
            
            badge.style.cursor = 'pointer';
            badge.title = 'Back to top';
        }
    }
    
    /**
     * Smooth scroll for anchor links
     */
    function initSmoothScroll() {
        const links = document.querySelectorAll('.theme-2026 a[href^="#"]');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Skip if it's just "#"
                if (href === '#') return;
                
                e.preventDefault();
                
                const targetElement = document.querySelector(href);
                
                if (targetElement) {
                    const offset = 80; // Account for fixed header if any
                    const targetPosition = targetElement.offsetTop - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    /**
     * Add loading state management
     */
    function initLoadingState() {
        window.addEventListener('load', function() {
            document.body.classList.add('loaded');
            
            // Trigger entrance animations
            const hero = document.querySelector('.theme-2026 .hero-modern');
            if (hero) {
                hero.classList.add('animate-in');
            }
        });
    }
    
    // Initialize loading state
    initLoadingState();
    
    // Export functions if needed
    window.Theme2026 = {
        initScrollAnimations: initScrollAnimations,
        initInteractiveCards: initInteractiveCards,
        initYearBadge: initYearBadge,
        initSmoothScroll: initSmoothScroll
    };
    
})();
