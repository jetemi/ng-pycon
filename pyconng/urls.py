from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from pyconng.views import year_page_serve
from home.views import NewsletterSignupView, SignupView, LoginView, LogoutView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("newsletter/signup/", NewsletterSignupView.as_view(), name="newsletter_signup"),
    
    # Authentication URLs
    path("accounts/signup/", SignupView.as_view(), name="signup"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    
    # Tickets (must be before Wagtail catch-all)
    path("tickets/", include("tickets.urls")),
    
    # CFP (must be before Wagtail catch-all)
    path("cfp/", include("cfp.urls")),

    # Travel Grants (must be before Wagtail catch-all)
    path("grants/", include("grants.urls")),

    # Dashboard (login required, current year only)
    path("dashboard/", include("dashboard.urls")),
    
    # Year-specific routing using custom view. Past years are read-only snapshots.
    path("<int:year>/search/", search_views.search, name="year_search"),
    path("<int:year>/", year_page_serve, {'path': ''}, name="year_home"),
    path("<int:year>/<path:path>/", year_page_serve, name="year_page"),
    
    # Root URL serves current year content directly (no redirect)
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
