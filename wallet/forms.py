from django import forms
from django.forms import TextInput
from .models import Savings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Create your forms here
class SavingsForm(forms.ModelForm):
    """Form used to create wallet with custom details"""

    class Meta:
        model = Savings
        fields = ["first_name", "last_name"]
        widgets = {
            "first_name": TextInput(attrs={"class": "mb-4"}),
            "last_name": TextInput(attrs={"class": "mb-4"}),
        }


class FundsForm(forms.Form):
    """Form used to fund and withdraw money from a wallet"""

    balance = forms.DecimalField(
        widget=TextInput(attrs={"class": "mb-4"}),
        help_text="Insert an amount into the field above.",
        label="Amount",
        label_suffix=" :",
        error_messages={"required": "This field cannot be empty."},
    )


class TransferForm(forms.Form):
    """Form used to transfer money to other users"""

    def validate_beneficiary_name(value):
        curr_val = value.strip()
        name = curr_val.split()
        if curr_val == "" or " " not in curr_val or len(name) > 2:
            raise ValidationError(
                _("Please enter a real beneficiary with a first name and last name."),
                code="invalid",
            )
        beneficiary_first_name, beneficiary_last_name = name
        try:
            Savings.objects.get(
                first_name__iexact=beneficiary_first_name,
                last_name__iexact=beneficiary_last_name,
            )
        except Savings.DoesNotExist:
            raise ValidationError(
                _("%(beneficiary)s does not exist. Please enter a real beneficiary."),
                code="invalid",
                params={"beneficiary": curr_val},
            )

    BANKS = [
        ("AC", "Access Bank"),
        ("GTB", "Guaranteed Trust Bank"),
        ("UBA", "UBA Bank"),
        ("FB", "First Bank"),
        ("FIDB", "Fidelity Bank"),
        ("SIBTC", "Stanbic IBTC Bank"),
        ("STB", "Sterling Bank"),
        ("WB", "Wema Bank"),
        ("UB", "Union Bank"),
        ("ZB", "Zenith Bank"),
    ]
    amount = forms.DecimalField(
        widget=TextInput(attrs={"class": "mb-4"}),
        help_text="Insert an amount into the field above.",
        label="Amount",
        label_suffix=" :",
        error_messages={"required": "This field cannot be empty."},
    )
    name = forms.CharField(
        help_text="Enter the full name of the beneficiary",
        widget=TextInput(attrs={"placeholder": "John Doe"}),
        label="Beneficiary Name",
        validators=[validate_beneficiary_name],
    )
    bank = forms.ChoiceField(
        help_text="Select the beneficiary's bank",
        label="Select a bank",
        choices=BANKS,
    )