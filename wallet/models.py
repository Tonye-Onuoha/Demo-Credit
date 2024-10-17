from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Savings(models.Model):
    """Model representing a savings wallet record."""

    first_name = models.CharField(
        help_text="Enter a first name to be used for your wallet",
        max_length=20,
        blank=False,
    )
    last_name = models.CharField(
        help_text="Enter a last name to be used for your wallet",
        max_length=20,
        blank=False,
    )
    balance = models.DecimalField(
        help_text="Enter your savings balance",
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        """Returns the URL to access the details for this savings record."""
        return reverse("savings-balance-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.first_name} {self.last_name} - {self.balance}"


class Transactions(models.Model):
    """Model representing a transaction record."""

    details = models.CharField(
        help_text="Enter the details of this transaction", max_length=50, blank=False
    )
    date = models.DateTimeField(auto_now_add=True)
    savings_id = models.ForeignKey(Savings, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        """Returns the URL to access the details for this transaction record."""
        return reverse("transaction-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.details}"