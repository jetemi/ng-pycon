// Alpine.js initialization
import Alpine from 'alpinejs'

// Alpine.js global data and functions
Alpine.data('navigation', () => ({
  isOpen: false,
  toggle() {
    this.isOpen = !this.isOpen
  },
  close() {
    this.isOpen = false
  }
}))

Alpine.data('theme', () => ({
  currentTheme: document.documentElement.dataset.theme || '2024',
  setTheme(theme) {
    this.currentTheme = theme
    document.documentElement.dataset.theme = theme
    localStorage.setItem('pycon-theme', theme)
  },
  init() {
    const savedTheme = localStorage.getItem('pycon-theme')
    if (savedTheme) {
      this.setTheme(savedTheme)
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
    form.addEventListener('submit', handleAjaxForm)
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
  notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`
  
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
