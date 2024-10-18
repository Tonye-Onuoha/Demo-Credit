from django.test import TestCase
from django.contrib.auth.models import User
from wallet.models import Savings, Transactions

# Create your tests here.
class SavingsModelTest(TestCase):
    """This subclass tests the model used for creating instances of a savings wallet."""

    @classmethod
    def setUpTestData(cls):
        # set up a user with a savings wallet for our tests.
        new_user = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="2HJ1vRV0Z&3iD"
        )
        Savings.objects.create(first_name="Jane", last_name="Doe", user_id=new_user)

    def test_first_name_label(self):
        savings_wallet = Savings.objects.get(id=1)
        label = savings_wallet._meta.get_field("first_name").verbose_name
        self.assertEqual(label, "first name")

    def test_first_name_max_length(self):
        savings_wallet = Savings.objects.get(id=1)
        max_length = savings_wallet._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 20)

    def test_first_name_help_text(self):
        savings_wallet = Savings.objects.get(id=1)
        help_text = savings_wallet._meta.get_field("first_name").help_text
        self.assertEqual(help_text, "Enter a first name to be used for your wallet")

    def test_last_name_label(self):
        savings_wallet = Savings.objects.get(id=1)
        label = savings_wallet._meta.get_field("last_name").verbose_name
        self.assertEqual(label, "last name")

    def test_last_name_max_length(self):
        savings_wallet = Savings.objects.get(id=1)
        max_length = savings_wallet._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 20)

    def test_last_name_help_text(self):
        savings_wallet = Savings.objects.get(id=1)
        help_text = savings_wallet._meta.get_field("last_name").help_text
        self.assertEqual(help_text, "Enter a last name to be used for your wallet")

    def test_balance_max_digits(self):
        savings_wallet = Savings.objects.get(id=1)
        max_digits = savings_wallet._meta.get_field("balance").max_digits
        self.assertEqual(max_digits, 12)

    def test_balance_decimal_places(self):
        savings_wallet = Savings.objects.get(id=1)
        decimal_places = savings_wallet._meta.get_field("balance").decimal_places
        self.assertEqual(decimal_places, 2)

    def test_balance_default_value(self):
        savings_wallet = Savings.objects.get(id=1)
        default_value = savings_wallet._meta.get_field("balance").default
        self.assertEqual(default_value, 0.00)

    def test_balance_help_text(self):
        savings_wallet = Savings.objects.get(id=1)
        help_text = savings_wallet._meta.get_field("balance").help_text
        self.assertEqual(help_text, "Enter your savings balance")

    def test_savings_first_name(self):
        savings_wallet = Savings.objects.get(id=1)
        expected_first_name = "Jane"
        self.assertEqual(expected_first_name, f"{savings_wallet.first_name}")

    def test_savings_last_name(self):
        savings_wallet = Savings.objects.get(id=1)
        expected_last_name = "Doe"
        self.assertEqual(expected_last_name, f"{savings_wallet.last_name}")

    def test_savings_user(self):
        savings_wallet = Savings.objects.get(id=1)
        expected_savings_user = User.objects.get(id=1)
        self.assertEqual(expected_savings_user, savings_wallet.user_id)

    def test_string_representation(self):
        savings_wallet = Savings.objects.get(id=1)
        expected_string = f'{savings_wallet.first_name} {savings_wallet.last_name} - {savings_wallet.balance}'
        self.assertEqual(expected_string, str(savings_wallet))


class TransactionsModelTest(TestCase):
    """This subclass tests the model used for creating instances of a transaction."""

    @classmethod
    def setUpTestData(cls):
        # set up a user with a savings wallet for our tests.
        new_user = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="2HJ1vRV0Z&3iD"
        )
        new_savings_wallet = Savings.objects.create(
            first_name="Jane", last_name="Doe", user_id=new_user
        )
        # set up a new transaction for the user's wallet.
        Transactions.objects.create(
            details="You funded your account with 1000 naira", savings_id=new_savings_wallet
        )

    def test_details_label(self):
        transaction = Transactions.objects.get(id=1)
        label = transaction._meta.get_field("details").verbose_name
        self.assertEqual(label, "details")

    def test_details_help_text(self):
        transaction = Transactions.objects.get(id=1)
        help_text = transaction._meta.get_field("details").help_text
        self.assertEqual(help_text, "Enter the details of this transaction")

    def test_details_max_length(self):
        transaction = Transactions.objects.get(id=1)
        max_length = transaction._meta.get_field("details").max_length
        self.assertEqual(max_length, 50)

    def test_details_value(self):
        transaction = Transactions.objects.get(id=1)
        expected_details = "You funded your account with 1000 naira"
        self.assertEqual(expected_details, f"{transaction.details}")

    def test_savings_id(self):
        transaction = Transactions.objects.get(id=1)
        expected_savings_id = Savings.objects.get(id=1)
        self.assertEqual(expected_savings_id, transaction.savings_id)

    def test_string_representation(self):
        transaction = Transactions.objects.get(id=1)
        expected_string = f"{transaction.details}"
        self.assertEqual(expected_string, str(transaction))
