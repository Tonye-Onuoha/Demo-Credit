from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("create-default/", views.default_wallet, name="create-default-wallet"),
    path("create-custom/", views.custom_wallet, name="create-custom_wallet"),
    path("fund-new/", views.new_funds, name="fund-new"),
    path("withdraw-funds/", views.withdraw_funds, name="withdraw-funds"),
    path("transfer-funds/", views.transfer_funds, name="transfer-funds"),
    path(
        "user-transactions/",
        views.UserTransactionsView.as_view(),
        name="user-transactions",
    ),
]
