# PyCon Nigeria Yearly Theming System

This directory contains the yearly theme files for the PyCon Nigeria website. Each year can have its own unique visual design while maintaining the same underlying functionality.

## File Structure

```
themes/
├── _base.css           # Base theming infrastructure and utility classes
├── 2024.css           # 2024 theme: "Tech Innovation" (Blue/Green)
├── 2025.css           # 2025 theme: "Creative Community" (Purple/Pink)
├── 2026.css           # 2026 theme: "Future Forward" (Teal/Blue/Orange)
└── README.md          # This file
```

## How It Works

### 1. Base Theme (`_base.css`)
- Defines CSS custom properties structure
- Provides theme-aware utility classes (`.bg-theme-primary`, `.text-theme-primary`, etc.)
- Sets up common components that all themes inherit

### 2. Year-Specific Themes
Each year gets its own CSS file with:
- Color palette definitions using CSS custom properties
- Year-specific design elements and animations
- Custom styling for components
- Unique visual effects

### 3. Theme Activation
Themes are activated using the `data-theme` attribute on the `<html>` element:

```html
<!-- 2024 theme -->
<html data-theme="2024">

<!-- 2025 theme -->
<html data-theme="2025">

<!-- 2026 theme -->
<html data-theme="2026">
```

## Current Themes

### 2024: "Tech Innovation"
- **Colors**: Blue (technology) + Green (growth) + Amber (energy)
- **Feel**: Professional, technological, sustainable
- **Animations**: Tech pulse effects, geometric patterns
- **File**: `2024.css`

### 2025: "Creative Community"
- **Colors**: Purple (creativity) + Pink (community) + Orange (enthusiasm)
- **Feel**: Creative, warm, community-focused
- **Animations**: Floating effects, rounded corners, creative gradients
- **File**: `2025.css`

### 2026: "Future Forward"
- **Colors**: Teal (innovation) + Blue (trust) + Orange (energy)
- **Feel**: Clean, modern, professional, forward-looking
- **Animations**: Smooth fade-ins, slide-ups, scale-ins
- **File**: `2026.css`
- **Inspiration**: PyCon US 2026 design language

## Creating a New Theme

### Step 1: Create the Theme File
Create a new file: `themes/YEAR.css`

```css
/* PyCon Nigeria YEAR Theme
 * Theme: "Your Theme Name" - Color Description
 * Color story: Your theme description
 */

[data-theme="YEAR"] {
  /* Primary color palette */
  --theme-primary: #your-color;
  --theme-primary-50: #lightest;
  --theme-primary-100: #lighter;
  /* ... continue with full palette */
  
  /* Secondary color palette */
  --theme-secondary: #your-color;
  /* ... full palette */
  
  /* Accent color palette */
  --theme-accent: #your-color;
  /* ... full palette */
}

/* Year-specific styles */
[data-theme="YEAR"] .theme-hero {
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-secondary));
}

/* Add more custom styles */
```

### Step 2: Import the Theme
Add the import to `input.css`:

```css
@import './themes/YEAR.css';
```

### Step 3: Update Theme Switching
Update the Alpine.js theme component in `pyconng.js` to include the new year.

## Available Theme Classes

### Color Utilities
- `.bg-theme-primary` - Primary background color
- `.text-theme-primary` - Primary text color
- `.border-theme-primary` - Primary border color
- `.bg-theme-secondary` - Secondary background color
- `.text-theme-secondary` - Secondary text color
- `.border-theme-secondary` - Secondary border color
- `.bg-theme-accent` - Accent background color
- `.text-theme-accent` - Accent text color
- `.border-theme-accent` - Accent border color

### Gradient Utilities
- `.bg-theme-gradient` - Theme gradient background
- `.text-theme-gradient` - Theme gradient text

### Component Classes
- `.theme-hero` - Hero section styling
- `.theme-card` - Card component styling
- `.theme-button` - Button styling
- `.theme-link` - Link styling
- `.theme-nav` - Navigation styling
- `.theme-footer` - Footer styling
- `.theme-heading` - Heading text styling

### Animation Classes (Year-specific)
- `.animate-tech-pulse` - 2024 tech pulse animation
- `.animate-creative-float` - 2025 creative float animation
- `.animate-fade-in` - 2026 fade-in animation
- `.animate-slide-up` - 2026 slide-up animation
- `.animate-scale-in` - 2026 scale-in animation

## Best Practices

### 1. Color Naming
Use consistent naming for CSS custom properties:
```css
--theme-primary-50   /* Lightest */
--theme-primary-100
--theme-primary-200
/* ... */
--theme-primary-500  /* Base color */
/* ... */
--theme-primary-900  /* Darkest */
```

### 2. Theme Scope
Always scope your styles to the year:
```css
[data-theme="2026"] .your-class {
  /* styles */
}
```

### 3. Fallbacks
The base theme provides fallbacks, but consider adding your own:
```css
background-color: #fallback-color;
background-color: var(--theme-primary);
```

### 4. Accessibility
Ensure sufficient color contrast in your theme:
- Test with tools like WebAIM Contrast Checker
- Provide alternative indicators beyond color
- Test with screen readers

## Development Workflow

1. **Design Phase**: Create mood boards and color palettes
2. **Development**: Build the theme file with all components
3. **Testing**: Test across different pages and components
4. **Integration**: Import and test the complete theme
5. **Documentation**: Update this README with your theme details

## Color Palette Tools

Recommended tools for creating cohesive color palettes:
- [Tailwind CSS Color Palette Generator](https://tailwindcss.com/docs/customizing-colors)
- [Coolors.co](https://coolors.co/)
- [Adobe Color](https://color.adobe.com/)
- [Material Design Color Tool](https://material.io/resources/color/)

## Browser Support

The theming system uses:
- CSS custom properties (supported in all modern browsers)
- CSS Grid and Flexbox
- CSS transforms and animations
- No IE11 support required 