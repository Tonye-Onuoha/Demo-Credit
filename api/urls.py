from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from .views import (
    register_user,
    savings_detail,
    create_savings,
    fund_savings,
    withdraw_funds,
    transfer_funds,
    user_transactions
)


urlpatterns = [
    path("register/", register_user, name="register-user"),
    #path("users/", users_list, name="users-list"), # remember to remove
   # path("savings/", savings_list, name="savings"), # remember to remove
    path("create-savings/", create_savings, name="create-savings"),
    path("savings-details/", savings_detail, name="savings-details"),
    path("fund-savings/", fund_savings, name="fund-savings"),
    path("withdraw-funds/", withdraw_funds, name="withdraw-funds"),
    path("transfer-funds/", transfer_funds, name="transfer-funds"),
    path("transactions/", user_transactions, name="user-transactions"),
]

urlpatterns = format_suffix_patterns(urlpatterns) # enables us to append format suffixes to endpoints.