from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from wallet.models import Savings, Transactions
from rest_framework import status

# The following classes handle tests for the API.


class RegisterUserAndLoginAPITests(APITestCase):
    """
    These tests ensure we can create a new user object and log in.
    """

    def test_register_user(self):
        url = "/api/register/"
        data = {
            "username": "john",
            "email": "johndoe@gmail.com",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # assert status code and response data.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"id": 1, "username": "john", "email": "johndoe@gmail.com"}
        )
        self.assertEqual(User.objects.count(), 1)
        expected_username = "john"
        self.assertEqual(User.objects.all().first().username, expected_username)

    def test_user_provides_invalid_credentials_during_login(self):
        # setup a user for our tests.
        User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR_FAKE_PASSWORD",  # invalid password
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_provides_valid_credentials_and_receives_token_after_successful_login(
        self,
    ):
        # setup a user for our tests.
        User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # assert token key is provided
        self.assertTrue("key" in response.data)


class CreateSavingsWalletAPITests(APITestCase):
    """
    These tests ensure we can create a new savings wallet for users.
    """

    @classmethod
    def setUpTestData(cls):
        # setup a user for our tests.
        User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )

    def test_user_not_authenticated(self):
        url = "/api/create-savings/"  # endpoint that requires authorization.
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user_creates_savings_wallet(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # create savings wallet.
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.post("/api/create-savings/", data, format="json")
        # assert status code and response data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"first_name": "John", "last_name": "Doe", "user_id": "john"}
        )
        # assert user now has savings wallet.
        savings = Savings.objects.all()
        self.assertEqual(len(savings), 1)
        expected_savings_owner = User.objects.all().first().username  # john
        self.assertEqual(savings.first().user_id.username, expected_savings_owner)


class CheckSavingsDetailsAPITests(APITestCase):
    """
    These tests ensure that users can check their savings wallet details.
    """

    @classmethod
    def setUpTestData(cls):
        # setup two users for our tests.
        user_1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        user_2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="1X<ISRUkw+tuK"
        )
        # setup a savings wallet for only the first user.
        Savings.objects.create(first_name="John", last_name="Doe", user_id=user_1)

    def test_user1_not_authenticated(self):
        url = "/api/savings-details/"  # endpoint that requires authorization.
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user1_has_savings_wallet(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # retrieve user savings wallet details.
        url = "/api/savings-details/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "first_name": "John",
                "last_name": "Doe",
                "balance": "0.00",
                "user_id": "john",
            },
        )

    def test_user2_has_no_savings_wallet(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "jane",
            "password": "1X<ISRUkw+tuK",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # retrieve user savings wallet details.
        url = "/api/savings-details/"
        response = self.client.get(url)
        # assert response is a bad request as user has no savings wallet.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "You do not have a savings wallet.")


class FundSavingsAPITests(APITestCase):
    """
    These tests ensure that users can fund their savings wallets.
    """

    @classmethod
    def setUpTestData(cls):
        # setup a new user for our test.
        new_user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        # setup a savings wallet for the new user.
        Savings.objects.create(first_name="John", last_name="Doe", user_id=new_user)

    def test_user_not_authenticated(self):
        url = "/api/fund-savings/"  # endpoint that requires authorization.
        data = {"amount": "500"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user_cannot_fund_savings_wallet_with_invalid_data(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # fund savings wallet.
        url = "/api/fund-savings/"
        data = {"amount": "INVALID_DATA"}  # invalid data
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["amount"][0], "A valid number is required.")

    def test_user_can_fund_savings_wallet_with_valid_data(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # fund user's savings wallet.
        url = "/api/fund-savings/"
        data = {"amount": "500"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "status": "success",
                "message": "You have successfully funded your account with 500.00 naira.",
            },
        )


class WithdrawFundsAPITests(APITestCase):
    """
    These tests ensure that users can withdraw funds from their savings wallets.
    """

    @classmethod
    def setUpTestData(cls):
        # setup a new user for our test.
        new_user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        # setup a savings wallet with initial balance of 500 for new user.
        Savings.objects.create(
            first_name="John", last_name="Doe", balance=500.00, user_id=new_user
        )

    def test_user_not_authenticated(self):
        url = "/api/withdraw-funds/"  # url for restricted resource
        data = {"amount": "100"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user_does_not_have_enough_funds(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # withdraw funds from savings wallet.
        url = "/api/withdraw-funds/"
        data = {"amount": "700"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0], "You do not have enough funds in your savings wallet."
        )

    def test_user_can_withdraw_funds(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # withdraw funds from savings wallet.
        url = "/api/withdraw-funds/"
        data = {"amount": "100"}
        response = self.client.put(url, data, format="json")
        # assert fund withdrawal from savings wallet.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        savings_wallet = Savings.objects.all().first()
        self.assertEqual(savings_wallet.balance, 400)
        transactions = Transactions.objects.all()
        # assert transactions on savings wallet.
        self.assertEqual(len(transactions), 1)
        self.assertEqual(
            transactions.first().details, "You withdrew 100.00 naira from your account."
        )
        self.assertEqual(
            response.data,
            {
                "status": "success",
                "message": "You have successfully withdrawn 100.00 naira from your account.",
            },
        )


class TransferFundsAPITests(APITestCase):
    """
    These tests ensure that users can transfer funds from their savings wallets.
    """

    def setUp(self):
        # set up two users for our tests.
        self.user1 = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="2HJ1vRV0Z&3iD"
        )
        self.user2 = User.objects.create_user(
            username="jane", email="janedoe@gmail.com", password="1X<ISRUkw+tuK"
        )
        # create a wallet with an amount of 1000 for one of the users.
        Savings.objects.create(
            first_name="John", last_name="Doe", balance=1000.00, user_id=self.user1
        )

    def test_user_not_authenticated(self):
        url = "/api/transfer-funds/"  # endpoint that requires authorization.
        data = {"amount": "300", "email": "janedoe@gmail.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_beneficiary_does_not_exist(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "2HJ1vRV0Z&3iD",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # transfer funds from savings wallet.
        url = "/api/transfer-funds/"  # endpoint that requires authorization.
        data = {"amount": "300", "email": "marydoe@gmail.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            "The beneficiary with email 'marydoe@gmail.com' does not exist.",
        )

    def test_beneficiary_does_not_have_a_savings_wallet(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "2HJ1vRV0Z&3iD",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # transfer funds from savings wallet.
        url = "/api/transfer-funds/"  # endpoint that requires authorization.
        data = {"amount": "300", "email": "janedoe@gmail.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0], "This beneficiary does not have a savings wallet."
        )

    def test_not_enough_funds_for_transfer(self):
        # create another wallet with an amount of 200 for the other user.
        Savings.objects.create(
            first_name="Jane", last_name="Doe", balance=200.00, user_id=self.user2
        )

        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "2HJ1vRV0Z&3iD",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # transfer funds from user's savings wallet.
        url = "/api/transfer-funds/"  # endpoint that requires authorization.
        data = {"amount": "1500", "email": "janedoe@gmail.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            "You do not have enough funds in your savings wallet for this transaction.",
        )

    def test_user_can_transfer_funds(self):
        # create another wallet with an amount of 200 for the other user.
        Savings.objects.create(
            first_name="Jane", last_name="Doe", balance=200.00, user_id=self.user2
        )

        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "2HJ1vRV0Z&3iD",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # transfer funds from user's savings wallet.
        url = "/api/transfer-funds/"  # endpoint that requires authorization.
        data = {"amount": "300", "email": "janedoe@gmail.com"}
        response = self.client.put(url, data, format="json")
        # assert transfer was successful.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "status": "success",
                "message": "You have successfully transferred 300.00 naira from your account to janedoe@gmail.com.",
            },
        )
        # retrieve both saving-wallets.
        user1_savings_wallet = Savings.objects.get(user_id=self.user1)
        user2_savings_wallet = Savings.objects.get(user_id=self.user2)
        # assert 300 has been deducted from user1.
        self.assertEqual(user1_savings_wallet.balance, 700.00)
        # assert 300 has been credited to user2.
        self.assertEqual(user2_savings_wallet.balance, 500.00)
        # assert two transactions have been created.
        transactions = Transactions.objects.all()
        self.assertEqual(len(transactions), 2)


class UserTransactionsAPITests(APITestCase):
    """
    These tests ensure that users can view all transactions on their savings wallets.
    """

    def setUp(self):
        # setup a new user for our test.
        self.user = User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )
        # setup a savings wallet with initial balance of 500 for new user.
        self.savings_wallet = Savings.objects.create(
            first_name="John", last_name="Doe", balance=500.00, user_id=self.user
        )

    def test_user_not_authenticated(self):
        url = "/api/transactions/"  # endpoint that requires authorization.
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user_has_zero_transactions(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # get user transactions.
        url = "/api/transactions/"
        response = self.client.get(url)
        # assert user has no available transactions.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "You do not have any transactions.")
        transactions = Transactions.objects.all()
        self.assertEqual(len(transactions), 0)

    def test_user_has_one_transaction(self):
        # create a transaction for our test user.
        Transactions.objects.create(
            details="You funded your account with 500 naira.",
            savings_id=self.savings_wallet,
        )
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # get user transactions.
        url = "/api/transactions/"
        response = self.client.get(url)
        # assert user has one available transaction.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["details"], "You funded your account with 500 naira."
        )
        transactions = Transactions.objects.all()
        self.assertEqual(len(transactions), 1)


class LogoutAPITests(APITestCase):
    """
    These tests ensure that users can log out successfully.
    """

    def setUp(self):
        # setup a new user for our test.
        User.objects.create_user(
            username="john", email="johndoe@gmail.com", password="LENDSQR001"
        )

    def test_user_can_login(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("key" in response.data)

    def test_user_can_logout(self):
        # login user to retrieve token key.
        url = "/api-dj-rest-auth/login/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # add token key to HTTP headers.
        token_key = response.data.get("key")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        # logout the user
        url = "/api-dj-rest-auth/logout/"
        data = {
            "username": "john",
            "password": "LENDSQR001",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully logged out.")
        # assert user cannot make further requests as token key is now invalid.
        response = self.client.get("/api/transactions/")
        self.assertEqual(str(response.data["detail"]), "Invalid token.")
