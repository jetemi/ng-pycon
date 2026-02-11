"""
Context processors for PyCon Nigeria website
"""
from django.conf import settings
from django.db.models import Q
from django.template.loader import get_template
from wagtail.models import Site
import re

# Available conference years and their themes
CONFERENCE_YEARS = {
    2024: {
        'theme': '2024',
        'name': 'Tech Innovation',
        'description': 'Clean, geometric, tech-focused design',
        'colors': ['#2563eb', '#059669', '#f59e0b'],
        'is_current': False,
    },
    2025: {
        'theme': '2025', 
        'name': 'Creative Community',
        'description': 'Organic, playful, community-focused design',
        'colors': ['#7c3aed', '#ec4899', '#ea580c'],
        'is_current': False,
    },
    2026: {
        'theme': '2026', 
        'name': 'Future Forward',
        'description': 'Clean, modern, professional, forward-looking design',
        'colors': ['#14b8a6', '#3b82f6', '#f97316'],
        'is_current': True,
    }
}

CURRENT_YEAR = 2026
DEFAULT_YEAR = CURRENT_YEAR

def conference_context(request):
    """
    Add conference year and theme information to template context
    """
    # Extract year from URL path
    year = None
    path = request.path
    
    # Match pattern like /2024/ or /2025/something
    year_match = re.match(r'^/(\d{4})/', path)
    if year_match:
        try:
            year = int(year_match.group(1))
        except ValueError:
            year = None
    
    # If no year in URL (root URL) or invalid year, use current year
    if year is None or year not in CONFERENCE_YEARS:
        year = CURRENT_YEAR
    
    year_info = CONFERENCE_YEARS.get(year, CONFERENCE_YEARS[CURRENT_YEAR])
    
    # Determine if this is a year-specific URL or root URL
    is_year_specific_url = year_match is not None
    
    # Determine which base template to use for this year.
    # Falls back to "base.html" if no year-specific base exists.
    base_template = f"base_{year}.html"
    try:
        get_template(base_template)
    except Exception:
        base_template = "base.html"
    
    context = {
        'conference_year': year,
        'conference_theme': year_info['theme'],
        'conference_year_info': year_info,
        'available_years': CONFERENCE_YEARS,
        'current_year': CURRENT_YEAR,
        'is_current_year': year == CURRENT_YEAR,
        'is_year_specific_url': is_year_specific_url,  # True for /2024/, False for /
        'base_template': base_template,  # e.g. "base_2026.html" or "base.html"
    }
    
    return context

def site_context(request):
    """
    Add general site information to template context
    """
    return {
        'site_name': 'PyCon Nigeria',
        'site_tagline': 'The premier Python conference in Nigeria',
        'debug': settings.DEBUG,
    }


def navigation_context(request):
    """
    Add navigation menu items to template context based on the current year.
    Gets navigation from HomePage - current year has conference_year=None/blank,
    archived years have conference_year set to the year.
    """
    # Extract year from URL path (same logic as conference_context)
    year = None
    path = request.path
    
    # Match pattern like /2024/ or /2025/something
    year_match = re.match(r'^/(\d{4})/', path)
    if year_match:
        try:
            year = int(year_match.group(1))
        except ValueError:
            year = None
    
    # If no year in URL (root URL) or invalid year, use current year
    if year is None or year not in CONFERENCE_YEARS:
        year = CURRENT_YEAR
    
    navigation_items = None
    page_year = None
    
    try:
        site = Site.find_for_request(request)
        if site:
            from home.models import HomePage
            
            if year == CURRENT_YEAR:
                # For current year, check if root_page itself is a HomePage (most common case)
                # The site's root_page is typically the current year's homepage
                root_page = site.root_page.specific
                if isinstance(root_page, HomePage):
                    # Check if this root homepage is for the current year
                    if (root_page.conference_year is None or 
                        root_page.conference_year == CURRENT_YEAR):
                        home_page = root_page
                    else:
                        home_page = None
                else:
                    home_page = None
                
                # If root_page is not the current year homepage, look for children
                if not home_page:
                    home_page = (
                        site.root_page.get_children()
                        .type(HomePage)
                        .live()
                        .filter(
                            # Current year homepage: conference_year is NULL/blank OR equals CURRENT_YEAR
                            Q(conference_year__isnull=True) | 
                            Q(conference_year=CURRENT_YEAR)
                        )
                        .first()
                    )
                
                # If still not found, try any HomePage with matching conference_year
                if not home_page:
                    home_page = (
                        HomePage.objects
                        .live()
                        .filter(
                            Q(conference_year__isnull=True) | 
                            Q(conference_year=CURRENT_YEAR)
                        )
                        .first()
                    )
                
                # Final fallback: if root_page is a HomePage, use it regardless of conference_year
                # This handles cases where the site root might be set to a different year
                if not home_page and isinstance(root_page, HomePage):
                    home_page = root_page
                
                if home_page:
                    # Ensure we have the specific instance (root_page.specific is already specific, but children need it)
                    if not isinstance(home_page, HomePage):
                        home_page = home_page.specific
                    navigation_items = home_page.navigation_menu_items
                    page_year = home_page.conference_year or CURRENT_YEAR
            else:
                # For archived years, get HomePage where conference_year matches the year
                home_page = (
                    HomePage.objects
                    .live()
                    .filter(conference_year=year)
                    .first()
                )
                
                # Also try by slug as fallback
                if not home_page:
                    home_page = (
                        HomePage.objects
                        .live()
                        .filter(slug=str(year))
                        .first()
                    )
                
                if home_page:
                    home_page = home_page.specific
                    navigation_items = home_page.navigation_menu_items
                    page_year = home_page.conference_year or year
    except Exception as e:
        # If there's any error, navigation_items will remain None
        # In production, you might want to log this
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting navigation for year {year}: {e}")
        pass
    
    return {
        'navigation_menu_items': navigation_items,
        'page_conference_year': page_year,  # The year of the page providing navigation
    } 