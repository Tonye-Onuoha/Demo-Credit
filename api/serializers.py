from rest_framework import serializers
from django.contrib.auth.models import User
from wallet.models import Savings, Transactions
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueValidator
from django.db.models import F
import requests


class UserSerializer(serializers.Serializer):
    def create(self, validated_data):
        new_username = validated_data.get("username")
        new_email = validated_data.get("email")
        new_password = validated_data.get("password")
        new_user = User.objects.create(username=new_username, email=new_email)
        new_user.set_password(new_password)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    def validate_email_not_blacklisted(value):
        """
        Validate that the user with this particular email has not been
        blacklisted.
        """
        
        url = f"https://adjutor.lendsqr.com/v2/verification/karma/{value}"
        api_key = "sk_live_52JLXbf8oEixCvuYat1qHUOtmBcjFwFM2NGbpzdG"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        json_response = response.json()
        if json_response["message"] == "Identity not found in karma ecosystem":
            return
        raise serializers.ValidationError("You have already been blacklisted.")

    id = serializers.IntegerField(label="ID", read_only=True)
    username = serializers.CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=150,
        validators=[
            UnicodeUsernameValidator,
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    email = serializers.EmailField(
        allow_blank=False,
        label="Email address",
        max_length=254,
        required=True,
        validators=[validate_email_not_blacklisted],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter a password",
        style={"input_type": "password", "placeholder": "Password"},
    )


class SavingsSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Savings
        fields = ["first_name", "last_name", "balance", "user_id"]


class CreateSavingsSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Savings
        fields = ["first_name", "last_name", "user_id"]

    def create(self, validated_data):
        first_name, last_name = (
            validated_data["first_name"],
            validated_data["last_name"],
        )
        savings_owner = validated_data["savings_owner"]
        try:
            savings_exists = Savings.objects.get(user_id=savings_owner)
            if savings_exists:
                raise serializers.ValidationError("You already have a savings account.")
        except Savings.DoesNotExist:
            savings_wallet = Savings.objects.create(
                first_name=first_name, last_name=last_name, user_id=savings_owner
            )
            return savings_wallet


class FundSavingsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, help_text="Enter an amount", max_digits=12, required=True
    )

    def save(self):
        amount = self.validated_data.get("amount")
        savings_owner = self.validated_data.get("savings_owner")
        try:
            savings_wallet = Savings.objects.get(user_id=savings_owner)
        except Savings.DoesNotExist:
            raise serializers.ValidationError("You do not have a savings wallet.")
        else:
            savings_wallet.balance = F("balance") + amount
            savings_wallet.save()
            Transactions.objects.create(
                details=f"You funded your account with {amount} naira.",
                savings_id=savings_wallet,
            )
            return savings_wallet


class WithdrawFundsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, help_text="Enter an amount", max_digits=12, required=True
    )

    def save(self):
        amount = self.validated_data.get("amount")
        savings_owner = self.validated_data.get("savings_owner")
        try:
            savings_wallet = Savings.objects.get(user_id=savings_owner)
        except Savings.DoesNotExist:
            raise serializers.ValidationError("You do not have a savings wallet.")
        else:
            if amount > savings_wallet.balance:
                raise serializers.ValidationError(
                    "You do not have enough funds in your savings wallet."
                )
            elif amount <= savings_wallet.balance:
                savings_wallet.balance = F("balance") - amount
                savings_wallet.save()
                Transactions.objects.create(
                    details=f"You withdrew {amount} naira from your account.",
                    savings_id=savings_wallet,
                )
                return savings_wallet


class TransferFundsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, help_text="Enter an amount", max_digits=12, required=True
    )
    email = serializers.EmailField(
        help_text="Enter an email address",
        max_length=None,
        min_length=None,
        allow_blank=False,
        required=True # all fields are required by default.
    )

    def save(self, request_user):
        amount = self.validated_data.get("amount")
        beneficiary_email = self.validated_data.get("email", None)
        remitter = request_user
        if beneficiary_email is None or beneficiary_email in set(["", " "]):
            raise serializers.ValidationError(
                "Please provide a valid email address."
            )
        try:
            beneficiary = User.objects.get(email=beneficiary_email)
            beneficiary_savings_wallet = Savings.objects.get(user_id=beneficiary)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f"The beneficiary with email '{beneficiary_email}' does not exist."
            )
        except Savings.DoesNotExist:
            raise serializers.ValidationError(
                "This beneficiary does not have a savings wallet."
            )
        else:
            remitter_savings_wallet = Savings.objects.get(user_id=remitter)
            if amount > remitter_savings_wallet.balance:
                raise serializers.ValidationError(
                    "You do not have enough funds in your savings wallet for this transaction."
                )
            elif amount <= remitter_savings_wallet.balance:
                remitter_savings_wallet.balance = F("balance") - amount
                remitter_savings_wallet.save()
                beneficiary_savings_wallet.balance = F("balance") + amount
                beneficiary_savings_wallet.save()
                Transactions.objects.create(
                    details=f"You transferred {amount} naira to {beneficiary.first_name} {beneficiary.last_name}.",
                    savings_id=remitter_savings_wallet,
                )
                Transactions.objects.create(
                    details=f"You were credited with {amount} naira from {remitter.first_name} {remitter.last_name}.",
                    savings_id=beneficiary_savings_wallet,
                )
                return remitter_savings_wallet
            
class TransactionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        fields = ["details", "date", "savings_id"]
