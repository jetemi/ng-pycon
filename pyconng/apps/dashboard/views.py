"""
Unified dashboard for PyCon Nigeria (current year only).

Role-based access: attendee, CFP reviewer, travel grant reviewer,
program chair, finance team, super admin.
"""

from django.shortcuts import redirect, render
from django.urls import reverse

from pyconng.context_processors import CURRENT_YEAR

from grants.models import GrantReviewerProfile, GrantReviewerAssignment
from grants.services import GrantService


def _get_cfp_context(user):
    """CFP reviewer/chair context. Returns None if CFP models unavailable."""
    try:
        from cfp.models import ReviewerProfile, ReviewerAssignment
        profile = ReviewerProfile.objects.filter(user=user, is_active=True).first()
        if not profile:
            return None
        assignments = ReviewerAssignment.objects.filter(reviewer=profile).select_related("proposal")
        return {
            "profile": profile,
            "assignment_count": assignments.count(),
        }
    except Exception:
        return None


def _get_cfp_open():
    try:
        from cfp.services import CFPService
        return CFPService.is_cfp_open()
    except Exception:
        return False


def dashboard(request):
    """Unified role-based dashboard. Login required. Current year only."""
    if not request.user.is_authenticated:
        return redirect(reverse("login") + f"?next={request.path}")

    grant_profile = None
    try:
        grant_profile = request.user.grant_reviewer_profile
    except GrantReviewerProfile.DoesNotExist:
        pass

    cfp_context = _get_cfp_context(request.user)

    roles = {
        "is_attendee": True,
        "is_cfp_reviewer": False,
        "is_cfp_chair": False,
        "is_grant_reviewer": False,
        "is_grant_chair": False,
        "is_finance": False,
        "is_super_admin": request.user.is_staff or request.user.is_superuser,
    }

    if cfp_context and cfp_context.get("profile"):
        p = cfp_context["profile"]
        roles["is_cfp_reviewer"] = p.is_active and not p.is_chair
        roles["is_cfp_chair"] = p.is_active and p.is_chair

    if grant_profile and grant_profile.is_active:
        roles["is_grant_reviewer"] = not grant_profile.is_chair
        roles["is_grant_chair"] = grant_profile.is_chair
        roles["is_finance"] = grant_profile.is_finance or grant_profile.is_chair

    grant_application = GrantService.get_user_application(request.user)
    grant_open = GrantService.is_grant_open()
    cfp_info = GrantService.get_user_cfp_info(request.user)
    cfp_open = _get_cfp_open()

    grant_assignment_count = 0
    if grant_profile and grant_profile.is_active:
        grant_assignment_count = GrantReviewerAssignment.objects.filter(
            reviewer=grant_profile
        ).count()

    context = {
        "conference_year": CURRENT_YEAR,
        "roles": roles,
        "grant_application": grant_application,
        "grant_open": grant_open,
        "grant_settings": GrantService.get_current_settings(),
        "cfp_info": cfp_info,
        "cfp_open": cfp_open,
        "cfp_context": cfp_context,
        "grant_assignment_count": grant_assignment_count,
    }

    return render(request, "dashboard/dashboard.html", context)
