"""Transactional email helper.

Renders an HTML + text pair from emails/<template>.{html,txt} and sends via
the configured EMAIL_BACKEND (Resend in production, console in dev).
"""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_email(
    *,
    template: str,
    to: list[str],
    subject: str,
    context: dict | None = None,
    tags: list[str] | None = None,
    reply_to: list[str] | None = None,
    fail_silently: bool = True,
    from_email: str | None = None,
) -> bool:
    """Render emails/<template>.html and .txt and send via configured backend.

    Returns True if a message was handed to the backend, False otherwise.
    Raises only when fail_silently is False.
    """
    ctx = {"site_name": "PyCon Nigeria", "support_email": "hello@pynigeria.com"}
    if context:
        ctx.update(context)

    try:
        text_body = render_to_string(f"emails/{template}.txt", ctx)
        html_body = render_to_string(f"emails/{template}.html", ctx)
    except Exception:
        logger.exception("Failed to render email template %r to %r", template, to)
        if not fail_silently:
            raise
        return False

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=to,
        reply_to=reply_to,
    )
    msg.attach_alternative(html_body, "text/html")
    if tags:
        msg.tags = list(tags)

    try:
        msg.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send email template=%r to=%r", template, to)
        if not fail_silently:
            raise
        return False
