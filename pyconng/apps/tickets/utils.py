import random
import string


def generate_order_code(length=12):
    """Generate a unique alphanumeric order code."""
    # Import here to avoid circular imports
    from .models import Ticket

    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Ticket.objects.filter(order=code).exists():
            return code
