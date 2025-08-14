from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.conf import settings
from django.template.loader import get_template
from wagtail.models import Page, Site
from home.models import HomePage
import os

ARCHIVE_DIR = os.path.join(settings.BASE_DIR, 'archives')


def _try_serve_static_archive(year: int, path: str):
    """Return HttpResponse for a static archived HTML if present; else None.
    Looks for files in BASE_DIR/archives/<year>/<path or index>.html
    """
    # Normalize path -> file path
    rel_path = path.strip('/')
    if rel_path == '':
        rel_path = 'index'
    # ensure .html
    if not rel_path.endswith('.html'):
        rel_path = f"{rel_path}.html"

    candidate = os.path.join(ARCHIVE_DIR, str(year), rel_path)
    if os.path.isfile(candidate):
        try:
            with open(candidate, 'r', encoding='utf-8') as f:
                html = f.read()
            return HttpResponse(html)
        except Exception:
            return None
    return None


def year_page_serve(request, year, path=''):
    """
    Custom view to handle year-based routing for Wagtail pages.
    If a static archive exists for the requested year, serve it as read-only.
    Otherwise, serve content from the current site's page tree without using the year in routing.
    """
    # 1) Static archive first (read-only past events)
    archive_response = _try_serve_static_archive(year, path)
    if archive_response is not None:
        return archive_response

    # 2) Dynamic fallback: serve from current site's tree
    try:
        site = Site.find_for_request(request)
        if not site:
            raise Http404("No site configured for this request")

        if path:
            routed = site.root_page.route(request, path.split('/'))
            if routed:
                page, args, kwargs = routed
            else:
                raise Http404("Page not found")
        else:
            # Find the designated home page (first live child or root)
            home_child = site.root_page.get_children().type(HomePage).live().first() if 'home' in settings.INSTALLED_APPS else None
            if home_child:
                page = home_child.specific
            else:
                page = site.root_page.specific
            args = ()
            kwargs = {}

        if not page.live:
            raise Http404("Page is not live")

        return page.serve(request, *args, **kwargs)

    except Exception as e:
        raise Http404(f"Page not found: {str(e)}") 
    