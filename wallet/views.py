from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Savings, Transactions
from .forms import SavingsForm, FundsForm, TransferForm
from django.views.generic import ListView
from django.db.models import F

# Create your views here.
class HomePageView(LoginRequiredMixin, ListView):
    """This view displays the user wallet homepage"""

    model = Savings
    context_object_name = "savings_wallet"
    template_name = "wallet/homepage.html"

    def get_queryset(self):
        try:
            savings_wallet = Savings.objects.get(user_id=self.request.user)
        except Savings.DoesNotExist:
            return None
        else:
            return savings_wallet

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the last five transactions.
        try:
            user_savings_wallet = Savings.objects.get(user_id=self.request.user)
            user_transactions = Transactions.objects.filter(savings_id=user_savings_wallet).order_by('-date')[:5]
        except Savings.DoesNotExist:
            context["transactions_history"] = None
        else:
            if not user_transactions:
                context["transactions_history"] = None
            else:
                context["transactions_history"] = user_transactions
        finally:
            return context


class UserTransactionsView(LoginRequiredMixin, ListView):
    """This view displays all the current user's past transactions"""

    model = Transactions
    context_object_name = "user_transactions"
    template_name = "wallet/transactions_list.html"
    
    def get_queryset(self):
        try:
            user_savings_wallet = Savings.objects.get(user_id=self.request.user)
            user_transactions = Transactions.objects.filter(savings_id=user_savings_wallet).order_by('-date')
        except Savings.DoesNotExist:
            return None
        else:
            return user_transactions


@login_required
def default_wallet(request):
    """This view renders a form to create a savings wallet with the current user's default credentials."""
    if request.method == "POST":
        new_wallet = Savings.objects.create(
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            user_id=request.user,
        )
        return redirect(reverse("home"))
    return render(request, "wallet/confirm_default.html")


@login_required
def custom_wallet(request):
    """This view renders a form to create a savings wallet with custom user credentials."""
    if request.method == "POST":
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings_wallet = form.save(commit=False)
            savings_wallet.user_id = request.user
            savings_wallet.save()
            return redirect(reverse("home"))
    else:
        form = SavingsForm()
    context = {"form": form}
    return render(request, "wallet/create_new.html", context)


@login_required
def new_funds(request):
    """This view renders a form to process funding of user wallets."""
    if request.method == "POST":
        savings_wallet = get_object_or_404(Savings, user_id=request.user)
        form = FundsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("balance")
            savings_wallet.balance = F("balance") + amount
            savings_wallet.save()
            Transactions.objects.create(
                details=f"You funded your account with {amount} naira",
                savings_id=savings_wallet,
            )
            return redirect(reverse("home"))
    else:
        form = FundsForm()
    context = {"form": form}
    return render(request, "wallet/fund_account.html", context)


@login_required
def withdraw_funds(request):
    """This view renders a form to process fund withdrawals."""
    if request.method == "POST":
        savings_wallet = get_object_or_404(Savings, user_id=request.user)
        form = FundsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("balance")
            savings_wallet.balance = F("balance") - amount
            savings_wallet.save()
            Transactions.objects.create(
                details=f"You withdrew {amount} naira from your account",
                savings_id=savings_wallet,
            )
            return redirect(reverse("home"))
    else:
        form = FundsForm()
    context = {"form": form}
    return render(request, "wallet/withdraw_funds.html", context)


BANKS = {
    "AC": "Access Bank",
    "GTB": "Guaranteed Trust Bank",
    "UBA": "UBA Bank",
    "FB": "First Bank",
    "FIDB": "Fidelity Bank",
    "SIBTC": "Stanbic IBTC Bank",
    "STB": "Sterling Bank",
    "WB": "Wema Bank",
    "UB": "Union Bank",
    "ZB": "Zenith Bank",
}


@login_required
def transfer_funds(request):
    """This renders a form to process funds transfer."""
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            beneficiary_firstname, beneficiary_lastname = name.split()
            amount = form.cleaned_data["amount"]
            bank = form.cleaned_data["bank"]
            beneficiary_bank = BANKS[bank]
            remitter_savings_wallet = get_object_or_404(Savings, user_id=request.user)
            remitter_savings_wallet.balance = F("balance") - amount
            remitter_savings_wallet.save()
            beneficiary_savings_wallet = get_object_or_404(
                Savings,
                first_name__iexact=beneficiary_firstname,
                last_name__iexact=beneficiary_lastname,
            )
            beneficiary_savings_wallet.balance = F("balance") + amount
            beneficiary_savings_wallet.save()
            Transactions.objects.create(
                details=f"You transferred {amount} naira to {beneficiary_savings_wallet.first_name.capitalize()} {beneficiary_savings_wallet.last_name.capitalize()} ({beneficiary_bank})",
                savings_id=remitter_savings_wallet,
            )
            Transactions.objects.create(
                details=f"You were credited with {amount} naira from {remitter_savings_wallet.first_name} {remitter_savings_wallet.last_name}",
                savings_id=beneficiary_savings_wallet,
            )
            return redirect(reverse("home"))
    else:
        form = TransferForm()
    context = {"form": form}
    return render(request, "wallet/transfer_funds.html", context)