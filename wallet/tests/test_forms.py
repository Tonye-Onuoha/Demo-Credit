from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from wallet.models import Savings
from wallet.forms import SavingsForm, FundsForm, TransferForm

# Create your tests here.
class SavingsFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for creating a wallet."""

    def test_first_name_label(self):
        form = SavingsForm()
        label = form.fields["first_name"].label
        self.assertTrue(label is None or label == "First name")

    def test_first_name_help_text(self):
        form = SavingsForm()
        help_text = form.fields["first_name"].help_text
        self.assertEqual(help_text, "Enter a first name to be used for your wallet")

    def test_last_name_label(self):
        form = SavingsForm()
        label = form.fields["last_name"].label
        self.assertTrue(label is None or label == "Last name")

    def test_last_name_help_text(self):
        form = SavingsForm()
        help_text = form.fields["last_name"].help_text
        self.assertEqual(help_text, "Enter a last name to be used for your wallet")

    def test_form_is_valid(self):
        data = {"first_name": "John", "last_name": "Doe"}
        form = SavingsForm(data)
        self.assertTrue(form.is_valid())


class FundsFormTest(SimpleTestCase):
    """This subclass tests the functionality of the form used for crediting and debiting wallets."""

    def test_balance_label(self):
        form = FundsForm()
        label = form.fields["balance"].label
        self.assertTrue(label == "Amount")

    def test_balance_help_text(self):
        form = FundsForm()
        help_text = form.fields["balance"].help_text
        self.assertEqual(help_text, "Insert an amount into the field above.")

    def test_balance_empty_value_error_message(self):
        data = {"balance": ""}
        form = FundsForm(data)
        form.is_valid()  # You can also access the error messages without having to call the is_valid() method first.
        self.assertEqual(form.errors["balance"], ["This field cannot be empty."])


class TransferFormTest(TestCase):
    """This subclass tests the functionality of the form used for funds transfer."""

    @classmethod
    def setUpTestData(cls):
        new_user = new_user = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="2HJ1vRV0Z&3iD"
        )
        Savings.objects.create(first_name="Jane", last_name="Doe", user_id=new_user)

    def test_amount_help_text(self):
        form = TransferForm()
        help_text = form.fields["amount"].help_text
        self.assertEqual(help_text, "Insert an amount into the field above.")

    def test_amount_label(self):
        form = TransferForm()
        label = form.fields["amount"].label
        self.assertTrue(label == "Amount")

    def test_amount_empty_value_error_message(self):
        data = {"amount": ""}
        form = TransferForm(data)
        form.is_valid()
        self.assertEqual(form.errors["amount"], ["This field cannot be empty."])

    def test_name_help_text(self):
        form = TransferForm()
        help_text = form.fields["name"].help_text
        self.assertEqual(help_text, "Enter the full name of the beneficiary")

    def test_name_label(self):
        form = TransferForm()
        label = form.fields["name"].label
        self.assertTrue(label == "Beneficiary Name")

    def test_name_is_invalid(self):
        data = {"amount": 100, "name": "fake name 419", "bank": "AC"}
        form = TransferForm(data)
        self.assertFalse(form.is_valid())

    def test_name_is_invalid_errors(self):
        data = {"amount": 100, "name": "fake name 419", "bank": "AC"}
        form = TransferForm(data)
        form.is_valid()
        self.assertEqual(
            form.errors["name"],
            ["Please enter a real beneficiary with a first name and last name."],
        )

    def test_bank_help_text(self):
        form = TransferForm()
        help_text = form.fields["bank"].help_text
        self.assertEqual(help_text, "Select the beneficiary's bank")

    def test_bank_label(self):
        form = TransferForm()
        label = form.fields["bank"].label
        self.assertTrue(label == "Select a bank")

    def test_form_is_valid(self):
        data = {"amount": 100, "name": "Jane Doe", "bank": "AC"}
        form = TransferForm(data)
        self.assertTrue(form.is_valid())