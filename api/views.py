from django.shortcuts import render
from django.contrib.auth.models import User
from wallet.models import Savings, Transactions
from .serializers import (
    UserSerializer,
    SavingsSerializer,
    CreateSavingsSerializer,
    FundSavingsSerializer,
    WithdrawFundsSerializer,
    TransferFundsSerializer,
    TransactionsSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

# Create your views here.
@api_view(["POST"])
def register_user(request, format=None):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_savings(request, format=None):
    if request.method == "POST":
        serializer = CreateSavingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(savings_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def savings_detail(request, format=None):
    if request.method == "GET":
        try:
            savings_wallet = Savings.objects.get(user_id=request.user)
        except Savings.DoesNotExist:
            raise serializers.ValidationError("You do not have a savings wallet.")
        else:
            serializer = SavingsSerializer(savings_wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def fund_savings(request, format=None):
    if request.method == "PUT":
        serializer = FundSavingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["savings_owner"] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def withdraw_funds(request, format=None):
    if request.method == "PUT":
        serializer = WithdrawFundsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["savings_owner"] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def transfer_funds(request, format=None):
    if request.method == "PUT":
        try:
            remitter_savings_wallet = Savings.objects.get(user_id=request.user)
        except Savings.DoesNotExist:
            raise serializers.ValidationError(
                "You cannot perform this transaction because you don't have a savings wallet."
            )
        else:
            serializer = TransferFundsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(request_user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_transactions(request, format=None):
    if request.method == "GET":
        try:
            user_savings_wallet = Savings.objects.get(user_id=request.user)
            user_transactions = Transactions.objects.filter(
                savings_id=user_savings_wallet
            )
        except Savings.DoesNotExist:
            raise serializers.ValidationError("You do not have a savings wallet.")
        else:
            if not user_transactions:
                raise serializers.ValidationError("You do not have any transactions.")
            serializer = TransactionsSerializer(user_transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
