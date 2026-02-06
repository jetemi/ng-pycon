# PyCon Nigeria Theme JavaScript

This directory contains JavaScript files for each conference year theme. Each theme has its own JS file with theme-specific interactions, animations, and functionality.

## Theme Files

| File | Year | Theme Name | Features | Description |
|------|------|------------|----------|-------------|
| `theme-2024.js` | 2024 | Tech Innovation | Scroll animations, card effects, countdown | Modern interactions with geometric focus |
| `theme-2025.js` | 2025 | Creative Community | Stagger animations, ripple effects | Bold, interactive effects |
| `theme-2026.js` | 2026 | Future Forward | Tilt effects, smooth scroll, year badge | Professional interactions |
| `theme-legacy.js` | Legacy | Classic Simplicity | Simple effects, print-friendly | Minimal, classic interactions |

## File Structure

Each theme JavaScript file includes:

1. **IIFE Wrapper** - Immediately Invoked Function Expression for scope isolation
2. **DOM Ready Check** - Waits for DOM before executing
3. **Feature Functions** - Modular functions for specific features
4. **Event Listeners** - User interaction handlers
5. **Exported API** - Public functions for external access

## Usage

Theme JavaScript files are automatically loaded based on the `theme` field:

```html
<!-- In theme template (e.g., theme_2024.html) -->
{% block extra_js %}
<script src="{% static 'js/themes/theme-2024.js' %}" defer></script>
{% endblock %}
```

## Common Features

### Scroll Animations
Animates elements when they come into viewport:

```javascript
function initScrollAnimations() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    });
    
    document.querySelectorAll('.feature-card').forEach(el => {
        observer.observe(el);
    });
}
```

### Interactive Cards
Adds hover and click effects to cards:

```javascript
function initInteractiveCards() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Add hover effect
        });
        
        card.addEventListener('mouseleave', () => {
            // Remove hover effect
        });
    });
}
```

### Smooth Scroll
Smooth scrolling for anchor links:

```javascript
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });
}
```

## Theme-Specific Features

### Theme 2024
- **Parallax Effect**: Hero section parallax on scroll
- **Countdown Timer**: Enhanced countdown display
- **Card Animations**: Fade-in animations with stagger

### Theme 2025
- **Ripple Effect**: Click ripple animations on cards
- **Stagger Animations**: Delayed animations for grid items
- **Mouse Tracking**: Mouse position effects on cards

### Theme 2026
- **Tilt Effect**: 3D tilt effect on card hover
- **Year Badge**: Interactive year badge with pulse
- **Loading State**: Entrance animations on page load

### Theme Legacy
- **Print Friendly**: Optimizes page for printing
- **Back to Top**: Adds back-to-top button for long pages
- **Simple Effects**: Minimal, classic interactions

## API Export

Each theme exports functions via the global `window` object:

```javascript
// Theme 2024
window.Theme2024 = {
    initScrollAnimations: initScrollAnimations,
    initInteractiveCards: initInteractiveCards
};

// Theme 2025
window.Theme2025 = {
    initScrollAnimations: initScrollAnimations,
    initInteractiveEffects: initInteractiveEffects,
    initStaggerAnimations: initStaggerAnimations
};

// Theme 2026
window.Theme2026 = {
    initScrollAnimations: initScrollAnimations,
    initInteractiveCards: initInteractiveCards,
    initYearBadge: initYearBadge,
    initSmoothScroll: initSmoothScroll
};

// Theme Legacy
window.ThemeLegacy = {
    initSimpleEffects: initSimpleEffects,
    initPrintFriendly: initPrintFriendly
};
```

### Usage from Console or External Scripts

```javascript
// Reinitialize animations
Theme2024.initScrollAnimations();

// Manually trigger effects
Theme2026.initYearBadge();
```

## Creating a New Theme JavaScript

To create a new theme JS file (e.g., for 2027):

### 1. Create the File

Create `theme-2027.js`:

```javascript
/**
 * PyCon Nigeria 2027 Theme JavaScript
 * Theme-specific interactions and animations
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('PyCon Nigeria 2027 Theme loaded');
        
        // Initialize features
        initYourFeature();
    });
    
    /**
     * Your feature function
     */
    function initYourFeature() {
        // Your code here
    }
    
    // Export functions
    window.Theme2027 = {
        initYourFeature: initYourFeature
    };
    
})();
```

### 2. Add to Template

In `home/templates/home/themes/theme_2027.html`:

```html
{% block extra_js %}
<script src="{% static 'js/themes/theme-2027.js' %}" defer></script>
{% endblock %}
```

## Best Practices

### 1. Scope Isolation
Always wrap code in IIFE to avoid global scope pollution:

```javascript
(function() {
    'use strict';
    // Your code here
})();
```

### 2. DOM Ready
Wait for DOM before executing:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize code
});
```

### 3. Event Delegation
Use event delegation for dynamic elements:

```javascript
document.body.addEventListener('click', function(e) {
    if (e.target.matches('.your-selector')) {
        // Handle event
    }
});
```

### 4. Performance
- Use `requestAnimationFrame` for animations
- Debounce scroll/resize handlers
- Remove event listeners when not needed
- Use Intersection Observer for scroll effects

### 5. Accessibility
- Respect `prefers-reduced-motion`
- Ensure keyboard navigation works
- Add appropriate ARIA attributes

```javascript
// Respect user motion preferences
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
    // Enable animations
}
```

### 6. Error Handling
```javascript
try {
    // Your code
} catch (error) {
    console.error('Theme error:', error);
}
```

## Performance Optimization

### Debouncing
```javascript
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Usage
window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Throttling
```javascript
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Usage
window.addEventListener('resize', throttle(handleResize, 200));
```

### Intersection Observer
```javascript
const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Element is visible
            }
        });
    },
    {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    }
);
```

## Browser Support

All theme JS files support:
- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ features (with transpilation if needed)
- Intersection Observer API
- CSS Transitions/Animations API

### Polyfills

For older browsers, consider:
- Intersection Observer polyfill
- smoothscroll-polyfill for smooth scrolling
- Event polyfills if needed

## Testing

Before deploying:

- [ ] Test in multiple browsers
- [ ] Test on mobile devices
- [ ] Verify no console errors
- [ ] Check performance (no jank)
- [ ] Test with JavaScript disabled (graceful degradation)
- [ ] Test accessibility features
- [ ] Verify animations respect motion preferences

## File Organization

```
pyconng/static/js/themes/
├── README.md              ← This file
├── theme-2024.js         ← 2024 theme JS
├── theme-2025.js         ← 2025 theme JS
├── theme-2026.js         ← 2026 theme JS
└── theme-legacy.js       ← Legacy theme JS
```

## Related Files

- CSS: `/pyconng/static/css/themes/`
- Templates: `/home/templates/home/themes/`
- Models: `/home/models.py`

## Debugging

### Console Logging
Each theme logs when loaded:

```javascript
console.log('PyCon Nigeria 2024 Theme loaded');
```

### Access Theme Functions
```javascript
// In browser console
Theme2024.initScrollAnimations();
```

### Check if Theme Loaded
```javascript
if (window.Theme2024) {
    console.log('Theme 2024 is loaded');
}
```

## Common Issues

### Issue: Animations Not Working
**Solution**: Check if CSS animation classes exist and are applied

### Issue: Event Listeners Not Firing
**Solution**: Verify DOM elements exist before adding listeners

### Issue: Performance Problems
**Solution**: Use debounce/throttle for frequent events

### Issue: Mobile Issues
**Solution**: Test touch events separately from mouse events

## Maintenance

- Review and update annually
- Remove unused code
- Optimize performance
- Update dependencies
- Keep browser compatibility current
- Monitor console for warnings/errors

---

**Last Updated**: February 2026  
**Maintainer**: PyCon Nigeria Development Team
