"""
Context processors for PyCon Nigeria website
"""
from django.conf import settings
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
    
    context = {
        'conference_year': year,
        'conference_theme': year_info['theme'],
        'conference_year_info': year_info,
        'available_years': CONFERENCE_YEARS,
        'current_year': CURRENT_YEAR,
        'is_current_year': year == CURRENT_YEAR,
        'is_year_specific_url': is_year_specific_url,  # True for /2024/, False for /
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