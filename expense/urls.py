
from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/createexpense/', ExpenseCreateView.as_view(), name='createexpense'),
    path('api/updateexpense/', ExpenseUpdateView.as_view(), name='updateexpense'),
    path('api/deleteexpense/', ExpenseDeleteView.as_view(), name='updateexpense'),
    path('api/listexpense/', ExpenseListView.as_view(), name='listexpense'),
]
