/**
 * PyCon Nigeria Legacy Theme JavaScript
 * Minimal JavaScript for classic, simple interactions
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('PyCon Nigeria Legacy Theme loaded');
        
        // Simple enhancements for legacy theme
        initSimpleEffects();
        initPrintFriendly();
    });
    
    /**
     * Simple hover and click effects
     */
    function initSimpleEffects() {
        // Add simple hover effect to feature boxes
        const featureBoxes = document.querySelectorAll('.theme-legacy .feature-box');
        
        featureBoxes.forEach(function(box) {
            box.addEventListener('mouseenter', function() {
                this.style.borderColor = '#e74c3c';
                this.style.transition = 'border-color 0.3s ease';
            });
            
            box.addEventListener('mouseleave', function() {
                this.style.borderColor = '#ddd';
            });
        });
        
        // Add click feedback to buttons
        const buttons = document.querySelectorAll('.theme-legacy .btn-classic');
        
        buttons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                // Simple scale effect
                this.style.transform = 'scale(0.95)';
                
                setTimeout(function() {
                    button.style.transform = '';
                }, 100);
            });
        });
    }
    
    /**
     * Make page more print-friendly
     */
    function initPrintFriendly() {
        // Before print, simplify page
        window.addEventListener('beforeprint', function() {
            console.log('Preparing page for print...');
            
            // Hide non-essential elements
            const archiveNotice = document.querySelector('.theme-legacy .archive-notice');
            if (archiveNotice) {
                archiveNotice.style.display = 'none';
            }
        });
        
        // After print, restore page
        window.addEventListener('afterprint', function() {
            console.log('Restoring page after print...');
            
            const archiveNotice = document.querySelector('.theme-legacy .archive-notice');
            if (archiveNotice) {
                archiveNotice.style.display = '';
            }
        });
    }
    
    /**
     * Simple smooth scroll (fallback for older browsers)
     */
    function initSimpleSmoothScroll() {
        const links = document.querySelectorAll('.theme-legacy a[href^="#"]');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                if (href === '#') return;
                
                const target = document.querySelector(href);
                
                if (target) {
                    e.preventDefault();
                    
                    // Simple scroll implementation
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    /**
     * Add "Back to Top" functionality
     */
    function initBackToTop() {
        // Check if page is long enough
        if (document.body.scrollHeight > window.innerHeight * 2) {
            // Create back to top button
            const backToTop = document.createElement('button');
            backToTop.textContent = '↑ Back to Top';
            backToTop.className = 'btn-classic btn-secondary';
            backToTop.style.cssText = 'position: fixed; bottom: 20px; right: 20px; display: none; z-index: 999;';
            
            document.body.appendChild(backToTop);
            
            // Show/hide based on scroll position
            window.addEventListener('scroll', function() {
                if (window.pageYOffset > 300) {
                    backToTop.style.display = 'inline-block';
                } else {
                    backToTop.style.display = 'none';
                }
            });
            
            // Scroll to top on click
            backToTop.addEventListener('click', function() {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }
    
    // Initialize back to top
    initBackToTop();
    initSimpleSmoothScroll();
    
    // Export functions if needed
    window.ThemeLegacy = {
        initSimpleEffects: initSimpleEffects,
        initPrintFriendly: initPrintFriendly
    };
    
})();
