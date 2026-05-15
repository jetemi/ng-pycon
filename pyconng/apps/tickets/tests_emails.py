from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TicketTransferEmailTests(TestCase):
    def setUp(self):
        mail.outbox = []
        User = get_user_model()
        self.old_owner = User.objects.create_user(
            username="alice", email="alice@example.com", password="pw"
        )
        self.new_owner = User.objects.create_user(
            username="bob", email="bob@example.com", password="pw"
        )

        from tickets.models import Ticket, TicketType, TicketSale
        self.ticket_type = TicketType.objects.create(
            name="Personal", price=Decimal("10.00"), conference_year=2026,
        )
        self.ticket = Ticket.objects.create(
            order="ORDER123",
            user=self.old_owner,
            ticket_type=self.ticket_type,
            quantity=1, amount=Decimal("10.00"), total_amount=Decimal("10.00"),
            status=Ticket.ISSUED,
            conference_year=2026,
        )
        self.ticket_sale = TicketSale.objects.create(
            ticket=self.ticket,
            user=self.old_owner,
            full_name="Alice Holder",
        )

    def test_transfer_sends_html_email_with_tags(self):
        from tickets.forms import TicketTransferForm
        form = TicketTransferForm(data={"email": "bob@example.com"})
        self.assertTrue(form.is_valid(), form.errors)
        form.save(self.ticket_sale)

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ["bob@example.com"])
        self.assertIn("Ticket Transfer", msg.subject)
        self.assertEqual(len(msg.alternatives), 1)
        html, _ = msg.alternatives[0]
        self.assertIn("alice@example.com", html)
        self.assertIn("Personal", html)
        self.assertEqual(msg.tags, ["tickets", "transfer"])


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TicketPurchaseConfirmationTests(TestCase):
    def setUp(self):
        mail.outbox = []
        User = get_user_model()
        self.user = User.objects.create_user(
            username="ada", email="ada@example.com", password="pw",
            first_name="Ada", last_name="Lovelace",
        )
        from tickets.models import Ticket, TicketType
        self.ticket_type = TicketType.objects.create(
            name="Personal", price=Decimal("10.00"), conference_year=2026,
        )
        self.ticket = Ticket.objects.create(
            order="ORDERAAA",
            user=self.user,
            ticket_type=self.ticket_type,
            quantity=2, amount=Decimal("10.00"), total_amount=Decimal("0"),
            status=Ticket.ISSUED,
            conference_year=2026,
        )

    def test_update_wallet_and_notify_sends_purchase_email(self):
        self.ticket.update_wallet_and_notify(Decimal("20.00"))
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ["ada@example.com"])
        self.assertIn("confirmed", msg.subject.lower())
        self.assertEqual(len(msg.alternatives), 1)
        html, _ = msg.alternatives[0]
        self.assertIn("Ada Lovelace", html)
        self.assertIn("Personal", html)
        self.assertIn("ORDERAAA", html)
        self.assertEqual(msg.tags, ["tickets", "purchase"])
