from django.test import TestCase
from django.contrib.auth.models import User
from wallet.models import Savings, Transactions
from django.urls import reverse

# Create your tests here.
class HomePageViewTest(TestCase):
    """This subclass is used to test the homepage view."""

    @classmethod
    def setUpTestData(cls):
        # set up a user for our tests.
        User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("home"))
        # assert current user is redirected to login page.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_user_logged_in(self):
        # log in the current user.
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("savings_wallet" in response.context)
        self.assertTrue("transactions_history" in response.context)
        self.assertEqual(str(response.context["user"]), "jane")
        # assert template and it's content.
        self.assertNotContains(response, "Wallet Balance")
        self.assertTemplateUsed(response, "wallet/homepage.html")

    def test_user_has_no_wallet(self):
        # log in the current user.
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("savings_wallet" in response.context)
        self.assertTrue("transactions_history" in response.context)
        self.assertEqual(str(response.context["user"]), "jane")
        # confirm user has no savings wallet.
        self.assertEqual(response.context["savings_wallet"], None)
        self.assertEqual(response.context["transactions_history"], None)
        # assert template and it's content.
        self.assertNotContains(response, "Wallet Balance")
        self.assertTemplateUsed(response, "wallet/homepage.html")

    def test_user_has_a_wallet(self):
        user = User.objects.get(id=1)
        new_savings_wallet = Savings.objects.create(
            first_name="Jane", last_name="Doe", user_id=user
        )
        # log in the current user.
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("savings_wallet" in response.context)
        self.assertTrue("transactions_history" in response.context)
        self.assertEqual(str(response.context["user"]), "jane")
        self.assertEqual(response.context["transactions_history"], None)
        # confirm user has a savings wallet
        self.assertEqual(response.context["savings_wallet"], new_savings_wallet)
        # assert template and it's content.
        self.assertContains(response, "Wallet Balance")
        self.assertTemplateUsed(response, "wallet/homepage.html")
        
    def test_user_has_multiple_transactions(self):
        # get the current user.
        curr_user = User.objects.get(id=1)
        # create a new wallet for the current user.
        curr_user_savings_wallet = Savings.objects.create(
            first_name="Jane", last_name="Doe", user_id=curr_user
        )
        # create multiple transactions for the current user.
        # - first transaction.
        first_transaction = Transactions.objects.create(details="You funded your account with 1000 naira", savings_id=curr_user_savings_wallet)
        # - second transaction.
        second_transaction = Transactions.objects.create(details="You withdrew 250 naira from your account", savings_id=curr_user_savings_wallet)
        # log in the current user.
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("savings_wallet" in response.context)
        self.assertTrue("transactions_history" in response.context)
        self.assertEqual(str(response.context["user"]), "jane")
        # confirm user has a savings wallet.
        self.assertEqual(response.context["savings_wallet"], curr_user_savings_wallet)
        # confirm user has two transactions.
        print(response.context["transactions_history"])
        self.assertQuerySetEqual(response.context["transactions_history"], [first_transaction, second_transaction])
        self.assertEqual(len(response.context["transactions_history"]), 2)
        # assert template and it's content.
        self.assertContains(response, "Wallet Balance")
        self.assertTemplateUsed(response, "wallet/homepage.html")


class DefaultWalletViewTest(TestCase):
    """This subclass tests the view responsible for creating the default savings wallet."""

    @classmethod
    def setUpTestData(cls):
        # set up a user for our test.
        User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")

    def test_user_creates_default_wallet(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/create-default/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "New wallet will be created with the following details:",
        )
        self.assertTemplateUsed(response, "wallet/create_default.html")
        response = self.client.post("/create-default/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/", status_code=302)


class CustomWalletViewTest(TestCase):
    """This subclass tests the view responsible for creating the custom savings wallet."""

    @classmethod
    def setUpTestData(cls):
        # set up a user for our tests.
        User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")

    def test_user_creates_blank_custom_wallet(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/create-custom/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Create New Wallet")
        self.assertTemplateUsed(response, "wallet/create_custom.html")
        response = self.client.post(
            "/create-custom/", {"first_name": "", "last_name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["first_name"], ["This field is required."]
        )
        self.assertEqual(
            response.context["form"].errors["last_name"], ["This field is required."]
        )

    def test_user_creates_valid_custom_wallet(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/create-custom/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Create New Wallet")
        self.assertTemplateUsed(response, "wallet/create_custom.html")
        response = self.client.post(
            "/create-custom/", {"first_name": "Jane", "last_name": "Doe"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/", status_code=302)
        # checks and asserts if new wallet has been created.
        new_savings_wallet = Savings.objects.all().first()
        self.assertEqual(new_savings_wallet.first_name, "Jane")
        self.assertEqual(new_savings_wallet.last_name, "Doe")
        # checks that owner of wallet is the current user ('request.user' not available via test client).
        self.assertEqual(new_savings_wallet.user_id, response.wsgi_request.user)


class NewFundsViewTest(TestCase):
    """This subclass tests the view responsible for handling the form used to fund a wallet."""

    @classmethod
    def setUpTestData(cls):
        # set up a user with a savings wallet for our tests.
        new_user = User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")
        # user wallet balance defaults to an amount of 0.00.
        Savings.objects.create(first_name="Jane", last_name="Doe", user_id=new_user)

    def test_user_submits_empty_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/fund-new/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Fund your account")
        self.assertTemplateUsed(response, "wallet/fund_account.html")
        response = self.client.post("/fund-new/", {"balance": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["balance"], ["This field cannot be empty."]
        )

    def test_user_submits_valid_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/fund-new/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Fund your account")
        self.assertTemplateUsed(response, "wallet/fund_account.html")
        response = self.client.post("/fund-new/", {"balance": "1000"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/", status_code=302)
        # retrieve the current user's savings wallet.
        user_savings_wallet = Savings.objects.get(id=1)
        # confirm savings wallet belongs to current user.
        self.assertEqual(user_savings_wallet.user_id, response.wsgi_request.user)
        # confirm current user's wallet balance now has an amount of 1000.
        self.assertEqual(int(user_savings_wallet.balance), 1000)
        # retrieve new transaction details.
        transaction = Transactions.objects.all().first()
        # confirm transaction details.
        self.assertEqual(
            f"{transaction.details}", "You funded your account with 1000 naira"
        )


class WithdrawFundsViewTest(TestCase):
    """This subclass tests the view responsible for handling the form used for fund withdrawals."""

    @classmethod
    def setUpTestData(cls):
        # set up a user for our tests.
        new_user = User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")
        # create a wallet with an amount of 1000 for the user.
        Savings.objects.create(
            first_name="Jane", last_name="Doe", balance=1000.00, user_id=new_user
        )

    def test_user_submits_empty_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/withdraw-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Withdraw Funds")
        self.assertTemplateUsed(response, "wallet/withdraw_funds.html")
        response = self.client.post("/withdraw-funds/", {"balance": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["balance"], ["This field cannot be empty."]
        )

    def test_user_submits_valid_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/withdraw-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Withdraw Funds")
        self.assertTemplateUsed(response, "wallet/withdraw_funds.html")
        response = self.client.post("/withdraw-funds/", {"balance": "300"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/", status_code=302)
        # retrieve the current user's savings wallet.
        user_savings_wallet = Savings.objects.get(id=1)
        # confirm savings wallet belongs to current user.
        self.assertEqual(user_savings_wallet.user_id, response.wsgi_request.user)
        # confirm current user's wallet balance now has an amount of 700 after a withdrawal of 300.
        self.assertEqual(int(user_savings_wallet.balance), 700)
        # retrieve new transaction details.
        transaction = Transactions.objects.all().first()
        # confirm transaction details.
        self.assertEqual(
            f"{transaction.details}", "You withdrew 300 naira from your account"
        )


class TransferFundsViewTest(TestCase):
    """This subclass tests the view responsible for handling the form used for funds transfer."""

    @classmethod
    def setUpTestData(cls):
        # set up two users for our tests.
        user1 = User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")
        user2 = User.objects.create_user(username="john", password="2HJ1vRV0Z&3iD")
        # create a wallet with an amount of 1000 for one of the users.
        Savings.objects.create(
            first_name="Jane", last_name="Doe", balance=1000.00, user_id=user1
        )
        # create another wallet with an amount of 200 for the other user.
        Savings.objects.create(
            first_name="John", last_name="Doe", balance=200.00, user_id=user2
        )

    def test_user_submits_empty_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/transfer-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Make a new transfer")
        self.assertTemplateUsed(response, "wallet/transfer_funds.html")
        response = self.client.post(
            "/transfer-funds/", {"amount": "", "name": "", "bank": "AC"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["amount"], ["This field cannot be empty."]
        )
        self.assertEqual(
            response.context["form"].errors["name"], ["This field is required."]
        )

    def test_user_submits_invalid_name(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/transfer-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Make a new transfer")
        self.assertTemplateUsed(response, "wallet/transfer_funds.html")
        response = self.client.post(
            "/transfer-funds/", {"amount": "300", "name": "fake name 419", "bank": "AC"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["name"],
            ["Please enter a real beneficiary with a first name and last name."],
        )

    def test_user_submits_non_existent_beneficiary(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/transfer-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Make a new transfer")
        self.assertTemplateUsed(response, "wallet/transfer_funds.html")
        response = self.client.post(
            "/transfer-funds/", {"amount": "300", "name": "Jack Doe", "bank": "AC"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors["name"],
            ["Jack Doe does not exist. Please enter a real beneficiary."],
        )

    def test_user_submits_valid_form(self):
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/transfer-funds/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertContains(response, "Make a new transfer")
        self.assertTemplateUsed(response, "wallet/transfer_funds.html")
        response = self.client.post(
            "/transfer-funds/", {"amount": "300", "name": "John Doe", "bank": "AC"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/", status_code=302)
        remitter_savings_wallet = Savings.objects.get(user_id=response.wsgi_request.user)
        beneficiary_savings_wallet = Savings.objects.get(first_name="John", last_name="Doe")
        # confirm 300 has been deducted from current user's savings wallet (formerly 1000).
        self.assertEqual(int(remitter_savings_wallet.balance), 700)
        # confirm 300 has been credited to other user's savings wallet (formerly 200).
        self.assertEqual(int(beneficiary_savings_wallet.balance), 500)
        # confirm transaction details.
        transaction = Transactions.objects.all().first()
        self.assertEqual(
            f"{transaction.details}",
            "You transferred 300 naira to John Doe (Access Bank)",
        )
        
class UserTransactionsViewTest(TestCase):
    """This subclass tests the view responsible for returning all the current user's past transactions."""
    
    @classmethod
    def setUpTestData(cls):
        # set up two users with a savings wallet for our tests.
        user_1 = User.objects.create_user(username="jane", password="1X<ISRUkw+tuK")
        user_2 = User.objects.create_user(username="john", password="2HJ1vRV0Z&3iD")
        # set up a wallet with a balance of 750.00 for user_1.
        user_1_savings_wallet = Savings.objects.create(first_name="Jane", last_name="Doe", balance=750.00, user_id=user_1)
        # create two transactions for user_1.
        # - first transaction.
        Transactions.objects.create(details="You funded your account with 1000 naira", savings_id=user_1_savings_wallet)
        # - second transaction.
        Transactions.objects.create(details="You withdrew 250 naira from your account", savings_id=user_1_savings_wallet)
        # set up a wallet with a balance of 100.00 for user_2.
        user_2_savings_wallet = Savings.objects.create(first_name="John", last_name="Doe", balance=100.00, user_id=user_2)
        # create one transaction for user_2.
        Transactions.objects.create(details="You funded your account with 400 naira", savings_id=user_2_savings_wallet)
        
        
    def test_user1_can_see_all_transactions(self):
        # log in as user_1.
        login = self.client.login(username="jane", password="1X<ISRUkw+tuK")
        response = self.client.get("/user-transactions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'jane')
        # assert user_1 has two transactions.
        self.assertEqual(len(response.context['user_transactions']), 2)
        # assert template and it's content.
        self.assertContains(response, "Past Transactions")
        self.assertTrue('user_transactions' in response.context)
        self.assertTemplateUsed(response, "wallet/transactions_list.html")
        
    def test_user2_can_see_all_transactions(self):
        # log in as user_2.
        login = self.client.login(username="john", password="2HJ1vRV0Z&3iD")
        response = self.client.get("/user-transactions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'john')
        # assert user_2 has one transaction.
        self.assertEqual(len(response.context['user_transactions']), 1)
        # assert template and it's content.
        self.assertContains(response, "Past Transactions")
        self.assertTrue('user_transactions' in response.context)
        self.assertTemplateUsed(response, "wallet/transactions_list.html")