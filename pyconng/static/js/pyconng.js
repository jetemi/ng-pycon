// Alpine.js initialization
import Alpine from 'alpinejs'

// Note: Navigation uses inline x-data in nav_header.html to avoid scope/store issues

Alpine.data('theme', (initialTheme = null) => ({
  currentTheme: '2026', // Default theme
  availableThemes: {
    '2024': {
      name: 'Tech Innovation',
      description: 'Clean, geometric, tech-focused design',
      colors: ['#2563eb', '#059669', '#f59e0b']
    },
    '2025': {
      name: 'Creative Community', 
      description: 'Organic, playful, community-focused design',
      colors: ['#7c3aed', '#ec4899', '#ea580c']
    },
    '2026': {
      name: 'Future Forward',
      description: 'Clean, modern, professional, forward-looking design',
      colors: ['#14b8a6', '#3b82f6', '#f97316']
    }
  },
  
  init() {
    // Get theme from URL/meta tags first, then localStorage, then default
    const urlTheme = this.getThemeFromMeta()
    const savedTheme = localStorage.getItem('pycon-theme')
    const urlParam = new URLSearchParams(window.location.search).get('theme')
    
    let themeToUse = null
    
    if (initialTheme && this.availableThemes[initialTheme]) {
      // Use theme passed from template (URL-based)
      themeToUse = initialTheme
    } else if (urlTheme && this.availableThemes[urlTheme]) {
      // Use theme from meta tag (URL-based year)
      themeToUse = urlTheme
    } else if (urlParam && this.availableThemes[urlParam]) {
      // Use theme from URL parameter
      themeToUse = urlParam
    } else if (savedTheme && this.availableThemes[savedTheme]) {
      // Use saved theme (but only if no URL-based theme)
      themeToUse = savedTheme
    } else {
      // Default theme
      themeToUse = '2026'
    }
    
    this.setTheme(themeToUse)
    
    console.log(`🎨 PyCon Nigeria ${themeToUse} theme loaded:`, this.availableThemes[themeToUse])
  },
  
  getThemeFromMeta() {
    const meta = document.querySelector('meta[name="conference-theme"]')
    return meta ? meta.content : null
  },
  
  setTheme(theme) {
    if (!this.availableThemes[theme]) {
      console.warn(`Theme "${theme}" not found. Using default.`)
      theme = '2026'
    }
    
    // Add transition class for smooth theme changes
    document.documentElement.classList.add('theme-transitioning')
    
    this.currentTheme = theme
    document.documentElement.dataset.theme = theme
    
    // Only save to localStorage if not URL-based theme
    const urlTheme = this.getThemeFromMeta()
    if (!urlTheme) {
      localStorage.setItem('pycon-theme', theme)
    }
    
    // Update meta theme color based on active theme
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.content = this.availableThemes[theme].colors[0]
    }
    
    // Remove transition class after animation
    setTimeout(() => {
      document.documentElement.classList.remove('theme-transitioning')
    }, 300)
    
    // Dispatch custom event for other components to react
    window.dispatchEvent(new CustomEvent('themeChanged', { 
      detail: { theme, themeData: this.availableThemes[theme] }
    }))
    
    console.log(`🎨 Switched to ${this.availableThemes[theme].name} theme`)
  },
  
  getThemeInfo(theme = null) {
    return this.availableThemes[theme || this.currentTheme]
  },
  
  navigateToYear(year) {
    // Navigate to different year URL
    // For current year, go to root URL; for other years, go to year-specific URL
    const currentYear = document.querySelector('meta[name="current-year"]')?.content
    if (year.toString() === currentYear) {
      window.location.href = `/`
    } else {
      window.location.href = `/${year}/`
    }
  }
}))

Alpine.data('modal', () => ({
  isOpen: false,
  open() {
    this.isOpen = true
    document.body.classList.add('overflow-hidden')
  },
  close() {
    this.isOpen = false
    document.body.classList.remove('overflow-hidden')
  }
}))

Alpine.data('countdown', (targetDate) => ({
  days: 0,
  hours: 0,
  minutes: 0,
  seconds: 0,
  interval: null,
  
  init() {
    this.updateCountdown()
    this.interval = setInterval(() => this.updateCountdown(), 1000)
  },
  
  updateCountdown() {
    const now = new Date().getTime()
    const target = new Date(targetDate).getTime()
    const difference = target - now
    
    if (difference > 0) {
      this.days = Math.floor(difference / (1000 * 60 * 60 * 24))
      this.hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      this.minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60))
      this.seconds = Math.floor((difference % (1000 * 60)) / 1000)
    } else {
      this.days = this.hours = this.minutes = this.seconds = 0
      if (this.interval) {
        clearInterval(this.interval)
      }
    }
  }
}))

// Start Alpine.js
Alpine.start()

// Custom JavaScript functions
document.addEventListener('DOMContentLoaded', function() {
  
  // Add smooth theme transition CSS
  const style = document.createElement('style')
  style.textContent = `
    .theme-transitioning * {
      transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
    }
  `
  document.head.appendChild(style)
  
  // Get conference data from meta tags
  const conferenceYear = document.querySelector('meta[name="conference-year"]')?.content
  const conferenceTheme = document.querySelector('meta[name="conference-theme"]')?.content
  const conferenceName = document.querySelector('meta[name="conference-name"]')?.content
  
  if (conferenceYear && conferenceTheme) {
    console.log(`🎉 PyCon Nigeria ${conferenceYear} (${conferenceName}) - Theme: ${conferenceTheme}`)
  }
  
  // Listen for theme changes
  window.addEventListener('themeChanged', function(event) {
    const { theme, themeData } = event.detail
    console.log(`🎨 Theme changed to: ${themeData.name}`)
    
    // Update any theme-dependent elements
    updateThemeDependentElements(theme)
  })
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href'))
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    })
  })

  // Scroll-triggered animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view')
      }
    })
  }, observerOptions)

  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el)
  })

  // Form enhancements
  const forms = document.querySelectorAll('form[data-ajax="true"]')
  forms.forEach(form => {
    if (form.id === 'newsletter-form') {
      form.addEventListener('submit', handleNewsletterForm)
    } else {
      form.addEventListener('submit', handleAjaxForm)
    }
  })

  // Lazy loading for images
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.classList.remove('opacity-0')
        img.classList.add('opacity-100')
        imageObserver.unobserve(img)
      }
    })
  })

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img)
  })

  // Header scroll behavior
  let lastScrollTop = 0
  const header = document.querySelector('header')
  
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      header?.classList.add('-translate-y-full')
    } else {
      // Scrolling up
      header?.classList.remove('-translate-y-full')
    }
    
    lastScrollTop = scrollTop
  })
})

// Update theme-dependent elements
function updateThemeDependentElements(theme) {
  // Update any elements that need special handling during theme changes
  const themeElements = document.querySelectorAll('[data-theme-element]')
  themeElements.forEach(element => {
    element.classList.add('theme-updating')
    setTimeout(() => {
      element.classList.remove('theme-updating')
    }, 300)
  })
}

// Newsletter form handler (sends JSON)
function handleNewsletterForm(event) {
  event.preventDefault()
  const form = event.target
  const emailInput = form.querySelector('#newsletter-email')
  const email = emailInput.value.trim()
  const submitBtn = form.querySelector('[type="submit"]')
  const messageDiv = document.getElementById('newsletter-message')
  
  if (!email) {
    if (messageDiv) {
      messageDiv.textContent = 'Please enter an email address.'
      messageDiv.className = 'mt-2 text-sm text-red-300'
    }
    return
  }
  
  // Show loading state
  const originalText = submitBtn.textContent
  submitBtn.textContent = 'Submitting...'
  submitBtn.disabled = true
  if (messageDiv) {
    messageDiv.textContent = ''
    messageDiv.className = 'mt-2 text-sm'
  }
  
  fetch(form.action, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ email: email })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showNotification(data.message, 'success')
      form.reset()
      if (messageDiv) {
        messageDiv.textContent = data.message
        messageDiv.className = 'mt-2 text-sm text-green-300'
      }
    } else {
      showNotification(data.message || 'An error occurred', 'error')
      if (messageDiv) {
        messageDiv.textContent = data.message || 'An error occurred'
        messageDiv.className = 'mt-2 text-sm text-red-300'
      }
    }
  })
  .catch(error => {
    const errorMsg = 'An error occurred. Please try again.'
    showNotification(errorMsg, 'error')
    if (messageDiv) {
      messageDiv.textContent = errorMsg
      messageDiv.className = 'mt-2 text-sm text-red-300'
    }
  })
  .finally(() => {
    submitBtn.textContent = originalText
    submitBtn.disabled = false
  })
}

// AJAX form handler
function handleAjaxForm(event) {
  event.preventDefault()
  const form = event.target
  const formData = new FormData(form)
  const submitBtn = form.querySelector('[type="submit"]')
  
  // Show loading state
  const originalText = submitBtn.textContent
  submitBtn.textContent = 'Submitting...'
  submitBtn.disabled = true
  
  fetch(form.action, {
    method: form.method,
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showNotification(data.message, 'success')
      form.reset()
    } else {
      showNotification(data.message || 'An error occurred', 'error')
    }
  })
  .catch(error => {
    showNotification('An error occurred. Please try again.', 'error')
  })
  .finally(() => {
    submitBtn.textContent = originalText
    submitBtn.disabled = false
  })
}

// Notification system
function showNotification(message, type = 'info') {
  const notification = document.createElement('div')
  notification.className = `fixed top-4 left-4 px-6 py-3 rounded-lg shadow-lg z-40 transform transition-all duration-300 translate-x-full`
  
  const colors = {
    success: 'bg-green-500 text-white',
    error: 'bg-red-500 text-white',
    warning: 'bg-yellow-500 text-white',
    info: 'bg-blue-500 text-white'
  }
  
  notification.className += ` ${colors[type]}`
  notification.textContent = message
  
  document.body.appendChild(notification)
  
  // Animate in
  setTimeout(() => {
    notification.classList.remove('translate-x-full')
  }, 100)
  
  // Remove after delay
  setTimeout(() => {
    notification.classList.add('translate-x-full')
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 5000)
}

// Theme switching utility functions
window.PyCon = {
  // Public API for theme switching
  switchTheme: function(theme) {
    const themeComponent = Alpine.$data(document.querySelector('[x-data*="theme"]'))
    if (themeComponent) {
      themeComponent.setTheme(theme)
    }
  },
  
  navigateToYear: function(year) {
    // Navigate to different year URL
    // For current year, go to root URL; for other years, go to year-specific URL
    const currentYear = document.querySelector('meta[name="current-year"]')?.content
    if (year.toString() === currentYear) {
      window.location.href = `/`
    } else {
      window.location.href = `/${year}/`
    }
  },
  
  getCurrentTheme: function() {
    return document.documentElement.dataset.theme
  },
  
  getCurrentYear: function() {
    const meta = document.querySelector('meta[name="conference-year"]')
    return meta ? parseInt(meta.content) : null
  },
  
  getAvailableThemes: function() {
    const themeComponent = Alpine.$data(document.querySelector('[x-data*="theme"]'))
    return themeComponent ? themeComponent.availableThemes : {}
  }
}

// Utility functions
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Export for potential use in other modules
export { showNotification, getCookie }
