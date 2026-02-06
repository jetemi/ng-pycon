# PyCon Nigeria Theme Stylesheets

This directory contains CSS files for each conference year theme. Each theme has its own complete stylesheet with all necessary styles, colors, typography, and animations.

## Theme Files

| File | Year | Theme Name | Primary Colors | Description |
|------|------|------------|----------------|-------------|
| `theme-2024.css` | 2024 | Tech Innovation | Blue (#3b82f6), Purple (#8b5cf6) | Modern, geometric, tech-focused design |
| `theme-2025.css` | 2025 | Creative Community | Emerald (#10b981), Indigo (#6366f1) | Bold, modern, community-focused design |
| `theme-2026.css` | 2026 | Future Forward | Teal (#14b8a6), Blue (#3b82f6) | Clean, professional, forward-looking design |
| `theme-legacy.css` | Legacy | Classic Simplicity | Dark Blue (#2c3e50), Red (#e74c3c) | Traditional, serif typography, timeless design |

## File Structure

Each theme CSS file includes:

1. **Font Imports** - Custom web fonts specific to the theme
2. **CSS Variables** - Theme-specific color palette and sizing
3. **Component Styles** - Styled components (cards, buttons, sections)
4. **Layout Styles** - Grid systems and responsive layouts
5. **Animations** - Custom animations and transitions
6. **Responsive Design** - Mobile-first breakpoints
7. **Utility Classes** - Helper classes for common patterns

## Usage

Theme stylesheets are automatically loaded based on the `theme` field in the HomePage model:

```html
<!-- In theme template (e.g., theme_2024.html) -->
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/themes/theme-2024.css' %}">
{% endblock %}
```

## CSS Class Naming Convention

Each theme uses a prefix class to scope styles:

- `.theme-2024` - 2024 theme
- `.theme-2025` - 2025 theme
- `.theme-2026` - 2026 theme
- `.theme-legacy` - Legacy theme

Example:
```css
.theme-2024 .hero-section {
    background: var(--theme-gradient-hero);
}

.theme-2024 .feature-card {
    border-radius: var(--theme-radius-lg);
}
```

## CSS Variables

Each theme defines CSS custom properties (variables) for easy customization:

### Typography Variables
```css
--theme-font-heading: 'Font Name', fallback;
--theme-font-body: 'Font Name', fallback;
```

### Color Variables
```css
--theme-primary: #hexcode;
--theme-secondary: #hexcode;
--theme-accent: #hexcode;
```

### Gradient Variables
```css
--theme-gradient-hero: linear-gradient(...);
--theme-gradient-card: linear-gradient(...);
```

### Shadow Variables
```css
--theme-shadow-sm: ...;
--theme-shadow-md: ...;
--theme-shadow-lg: ...;
--theme-shadow-xl: ...;
```

### Border Radius Variables
```css
--theme-radius-sm: ...;
--theme-radius-md: ...;
--theme-radius-lg: ...;
--theme-radius-xl: ...;
```

## Responsive Breakpoints

All themes follow mobile-first responsive design:

- **Mobile**: Default styles (up to 768px)
- **Tablet**: 768px and up
- **Desktop**: 1024px and up
- **Large Desktop**: 1280px and up

Example:
```css
/* Mobile-first */
.theme-2024 .section {
    padding: 2rem 0;
}

/* Tablet and up */
@media (min-width: 768px) {
    .theme-2024 .section {
        padding: 4rem 0;
    }
}
```

## Creating a New Theme

To create a new theme stylesheet (e.g., for 2027):

1. **Create the file**: `theme-2027.css`

2. **Import fonts** (optional):
```css
@import url('https://fonts.googleapis.com/css2?family=...');
```

3. **Define variables**:
```css
.theme-2027 {
    --theme-primary: #yourcolor;
    --theme-secondary: #yourcolor;
    /* ... more variables */
}
```

4. **Add component styles**:
```css
.theme-2027 .hero-section { /* styles */ }
.theme-2027 .feature-card { /* styles */ }
/* ... more components */
```

5. **Add responsive styles**:
```css
@media (max-width: 768px) {
    .theme-2027 .hero-section { /* mobile styles */ }
}
```

6. **Update the HomePage model** in `home/models.py`:
```python
THEME_CHOICES = [
    # ... existing themes ...
    ('theme_2027', '2027 Theme'),
]
```

7. **Create corresponding template** in `home/templates/home/themes/theme_2027.html`

## Performance Considerations

### File Size
- Keep CSS files under 100KB when minified
- Use CSS variables for repeated values
- Avoid deeply nested selectors

### Loading
- Themes are loaded via `<link>` tags (not inline)
- Browsers can cache theme CSS files
- Use `defer` or `async` where appropriate

### Optimization
- Minify CSS in production
- Use CDN for font files when possible
- Compress images referenced in CSS
- Use CSS containment where appropriate

## Browser Support

All theme CSS files support:
- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox
- CSS Custom Properties (variables)
- CSS Animations and Transitions

### Fallbacks
- Legacy theme includes print styles
- Graceful degradation for older browsers
- Progressive enhancement approach

## Best Practices

1. **Scope all styles** - Use theme class prefix (e.g., `.theme-2024`)
2. **Use CSS variables** - For maintainability and theming
3. **Mobile-first** - Start with mobile styles, enhance for larger screens
4. **Semantic naming** - Clear, descriptive class names
5. **Comment sections** - Use comment blocks to organize CSS
6. **Consistent spacing** - Follow established spacing system
7. **Reusable patterns** - Create utility classes for common styles

## Testing

Before deploying a new theme:

- [ ] Test on multiple screen sizes
- [ ] Verify colors meet accessibility standards (WCAG AA)
- [ ] Check font loading and fallbacks
- [ ] Test animations and transitions
- [ ] Verify responsive breakpoints
- [ ] Check print styles (legacy theme)
- [ ] Test in different browsers
- [ ] Validate CSS syntax

## File Organization

```
pyconng/static/css/themes/
├── README.md              ← This file
├── theme-2024.css        ← 2024 theme styles
├── theme-2025.css        ← 2025 theme styles
├── theme-2026.css        ← 2026 theme styles
└── theme-legacy.css      ← Legacy theme styles
```

## Related Files

- JavaScript: `/pyconng/static/js/themes/`
- Templates: `/home/templates/home/themes/`
- Models: `/home/models.py` (THEME_CHOICES)

## Maintenance

- Review and update themes annually
- Remove unused styles
- Optimize for performance
- Update browser compatibility
- Keep dependencies (fonts) up to date

---

**Last Updated**: February 2026  
**Maintainer**: PyCon Nigeria Development Team
