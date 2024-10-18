from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    users_list,
    register_user,
    savings_list,
    savings_detail,
    create_savings,
    fund_savings,
    withdraw_funds,
    transfer_funds,
    user_transactions
)

schema_view = get_schema_view(
    openapi.Info(
        title="Demo Credit API",
        default_version="v1",
        description="An API for Demo Credit",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("users/", users_list, name="users-list"), # remember to remove
    path("savings/", savings_list, name="savings"), # remember to remove
    path("create-savings/", create_savings, name="create-savings"),
    path("savings-details/", savings_detail, name="savings-details"),
    path("fund-savings/", fund_savings, name="fund-savings"),
    path("withdraw-funds/", withdraw_funds, name="withdraw-funds"),
    path("transfer-funds/", transfer_funds, name="transfer-funds"),
    path("transactions/", user_transactions, name="user-transactions"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns) # enables us to append format suffixes to endpoints.