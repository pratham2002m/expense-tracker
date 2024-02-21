from django.db import models
from django.utils import timezone
from django import forms
import uuid

class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=20, null=False, blank=False )
    

    def __str__(self):
        return self.username


class Expense(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False )
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=2000)
    category = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
