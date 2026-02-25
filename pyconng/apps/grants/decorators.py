"""
Permission decorators for the Travel Grant system.

    @grant_open_required     - Applications must be open
    @login_required          - User must be logged in (Django auth)
    @grant_reviewer_required - Grant reviewer (or chair)
    @grant_chair_required    - Grant chair only
    @grant_finance_required  - Finance team (or chair)
"""

from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import GrantReviewerProfile
from .services import GrantService


def grant_open_required(view_func):
    """Redirect to grants:closed if applications are not open."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not GrantService.is_grant_open():
            return redirect("grants:closed")
        return view_func(request, *args, **kwargs)

    return _wrapped


def login_required(view_func):
    """Require Django authentication."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped


def _get_grant_profile(request):
    """Get GrantReviewerProfile if user has one; None otherwise."""
    if not request.user.is_authenticated:
        return None
    try:
        return request.user.grant_reviewer_profile
    except GrantReviewerProfile.DoesNotExist:
        return None


def grant_reviewer_required(view_func):
    """Require grant reviewer role (reviewer or chair)."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        profile = _get_grant_profile(request)
        if not profile or not profile.is_active:
            return HttpResponseForbidden("You do not have permission to access this page.")
        request.grant_profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped


def grant_chair_required(view_func):
    """Require grant chair role."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        profile = _get_grant_profile(request)
        if not profile or not profile.is_active or not profile.is_chair:
            return HttpResponseForbidden("Only chairs can access this page.")
        request.grant_profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped


def grant_finance_required(view_func):
    """Require finance team role (finance or chair)."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        profile = _get_grant_profile(request)
        if not profile or not profile.is_active:
            return HttpResponseForbidden("You do not have permission to access this page.")
        if not profile.is_finance and not profile.is_chair:
            return HttpResponseForbidden("You do not have permission to access this page.")
        request.grant_profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped
