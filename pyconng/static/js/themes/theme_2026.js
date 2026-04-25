/**
 * PyCon Nigeria 2026 Theme — scroll reveals, hero ready state, smooth anchors
 */
(function() {
    'use strict';

    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function initScrollReveals() {
        if (prefersReducedMotion()) {
            document.querySelectorAll('.js-reveal-2026').forEach(function (el) {
                el.classList.add('is-visible');
            });
            return;
        }

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -5% 0px' }
        );

        document.querySelectorAll('.theme-2026 .js-reveal-2026').forEach(function (el) {
            observer.observe(el);
        });
    }

    function initHeroReady() {
        var hero = document.querySelector('.theme-2026 .hero-2026');
        if (!hero) {
            return;
        }
        if (document.readyState === 'complete' || prefersReducedMotion()) {
            hero.classList.add('hero-2026--ready');
            return;
        }
        window.addEventListener('load', function onLoad() {
            window.removeEventListener('load', onLoad);
            hero.classList.add('hero-2026--ready');
        });
    }

    function initYearBadge() {
        var badge = document.querySelector('.theme-2026 .year-badge');
        if (!badge) {
            return;
        }
        badge.addEventListener('mouseenter', function () {
            this.classList.add('pulse-on-hover');
        });
        badge.addEventListener('mouseleave', function () {
            this.classList.remove('pulse-on-hover');
        });
        badge.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
        });
        badge.style.cursor = 'pointer';
        badge.title = 'Back to top';
    }

    function initSmoothScroll() {
        if (prefersReducedMotion()) {
            return;
        }
        var links = document.querySelectorAll('.theme-2026 a[href^="#"]');
        links.forEach(function (link) {
            link.addEventListener('click', function (e) {
                var href = this.getAttribute('href');
                if (!href || href === '#') {
                    return;
                }
                var target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    var offset = 80;
                    var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                    window.scrollTo({ top: top, behavior: 'smooth' });
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initScrollReveals();
        initHeroReady();
        initYearBadge();
        initSmoothScroll();
    });

    window.Theme2026 = {
        initScrollReveals: initScrollReveals,
        initHeroReady: initHeroReady,
        initYearBadge: initYearBadge,
        initSmoothScroll: initSmoothScroll
    };
})();
