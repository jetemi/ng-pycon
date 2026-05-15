"""Travel grant transactional emails."""
from __future__ import annotations

from emails.services import send_email


def send_grant_submission_confirmation(application) -> None:
    user = application.user
    if not user or not user.email:
        return
    send_email(
        template="grants/submission_confirmation",
        to=[user.email],
        subject="PyCon Nigeria Travel Grant — Application Received",
        context={
            "applicant_name": user.get_full_name() or user.email,
            "conference_year": application.conference_year,
            "dashboard_url": "https://pycon.ng/grants/",
        },
        tags=["grants", "submission"],
        fail_silently=True,
    )


def send_grant_decision(application) -> None:
    """Send approval or rejection email based on application.status."""
    from grants.models import TravelGrantApplication

    user = application.user
    if not user or not user.email:
        return

    if application.status == TravelGrantApplication.STATUS_APPROVED:
        template = "grants/approved"
        subject = "PyCon Nigeria Travel Grant — Approved"
        decision_tag = "approved"
        extra_context = {"approved_amount": application.approved_amount}
    elif application.status == TravelGrantApplication.STATUS_NOT_SELECTED:
        template = "grants/rejected"
        subject = "PyCon Nigeria Travel Grant — Decision"
        decision_tag = "rejected"
        extra_context = {}
    else:
        return  # Waitlist and other statuses: no email for now.

    send_email(
        template=template,
        to=[user.email],
        subject=subject,
        context={
            "applicant_name": user.get_full_name() or user.email,
            "conference_year": application.conference_year,
            "dashboard_url": "https://pycon.ng/grants/",
            **extra_context,
        },
        tags=["grants", "decision", decision_tag],
        fail_silently=True,
    )
