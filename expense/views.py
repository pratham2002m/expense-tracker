from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserModel, Expense
from .serializers import ExpenseSerializer  # Import your ExpenseSerializer


class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = UserModel.objects.get(username=username, password=password)
            return JsonResponse({"response": "Login successful"}, status=200)
        except Exception as e:
            return JsonResponse({"response": "Invalid credentials"}, status=401)

class RegistrationView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            password = request.data.get('password')
            user = UserModel.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
            user.save()
            return JsonResponse({"response": "User has been registered successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"response": str(e)}, status=401)

class ExpenseCreateView(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = UserModel.objects.get(username=username)
        amount = request.data.get('amount')
        text = request.data.get('text')
        category = "Income" if amount > 0 else "Expense"
        payment_mode = request.data.get('payment_mode')

        expense = Expense.objects.create(user=user, amount=amount, text=text, category=category, payment_mode=payment_mode)
        expense.save()

        return Response({"response": "Transaction created successfully"}, status=status.HTTP_201_CREATED)

class ExpenseUpdateView(APIView):
    def post(self, request):
        id = request.data.get('id')

        username = request.data.get('username')
        user = UserModel.objects.get(username=username)
        amount = request.data.get('amount')
        text = request.data.get('text')
        category = "Income" if amount > 0 else "Expense"
        payment_mode = request.data.get('payment_mode')

        Expense.objects.update(id=id, user=user, amount=amount, text=text, category=category, payment_mode=payment_mode)

        return Response({"response": "Transaction updated successfully"}, status=status.HTTP_201_CREATED)


class ExpenseDeleteView(APIView):
    def delete(self, request):
        id = request.data.get('id')
        Expense.objects.get(id=id).delete()
        return Response({"response": "Transaction deleted successfully"}, status=status.HTTP_201_CREATED)


class ExpenseListView(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(UserModel, username=username)

        if 'type' in request.data:
            category = request.data['type']


            expenses = Expense.objects.filter(user=user, category=category)

            

            if expenses:

                if 'sortby' in request.data:
                    sortby = request.data.get('sortby')
                    expenses = expenses.order_by(sortby)

                serializer = ExpenseSerializer(expenses, many=True)
                serialized_data = serializer.data

                return Response({"response": serialized_data}, status=status.HTTP_200_OK)
            else:
                return Response({"response": "No such transactions found."}, status=status.HTTP_404_NOT_FOUND)

        expenses = Expense.objects.filter(user=user)
        if expenses:
            if 'sortby' in request.data:
                sortby = request.data.get('sortby')
                expenses = expenses.order_by(sortby)

            serializer = ExpenseSerializer(expenses, many=True)
            serialized_data = serializer.data

        return Response({"response": serialized_data}, status=status.HTTP_200_OK)