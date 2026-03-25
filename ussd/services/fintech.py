from django.db import transaction

from ussd.models import User, Account, Transaction


def get_balance(phone_number: str) -> float:
    """ Gets and returns a users account balance """
    user = User.objects.get(phone_number=phone_number)
    account = Account.objects.get(user=user)

    return account.balance


@transaction.atomic
def handle_transfer(sender_phone_number: str, receiver_phone_number: str, amount: float) -> tuple[bool, str]:
    """ Handles a transfer from a sender to a receiver """
    try:
        sender = User.objects.get(phone_number=sender_phone_number)
        receiver = User.objects.get(phone_number=receiver_phone_number)

        sender_account = Account.objects.get(user=sender)
        receiver_account = Account.objects.get(user=receiver)

        if sender_account.balance < amount:
            return False, "Insufficient funds"

        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            transaction_type='debit',
            status='success'
        )

        return True, "Transfer successful"
    except Exception as e:
        return False, str(e)
