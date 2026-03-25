from django.db import models


# Create your models here.
class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone_number


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"Account for {self.user.phone_number}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.phone_number} to {self.receiver.phone_number} - {self.amount}"


class UssdSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    data = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"USSD Session for {self.phone_number}"
