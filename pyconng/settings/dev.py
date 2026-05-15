import os

from .base import *
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Use console backend by default in dev so emails print to stdout.
# Set USE_RESEND_IN_DEV=True in .env to actually hit Resend during local testing.
if os.environ.get("USE_RESEND_IN_DEV", "").lower() in ("1", "true", "yes"):
    EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
