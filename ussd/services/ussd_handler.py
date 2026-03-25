from ussd.models import UssdSession, User, Account
from ussd.services.fintech import get_balance, handle_transfer
from ussd.services.session_manager import update_session, clear_session


def ussd_handler(session: UssdSession, text: str, phone_number: str) -> str:
    """ Handle USSD requests and interactions """
    data = session.data

    if text == "":
        return "CON Welcome\n1. Check Balance\n2. Transfer"

    inputs = text.split("*")

    if inputs[0] == "1":
        balance = get_balance(phone_number)
        clear_session(session)
        return f"END Your balance is {balance}"

    elif inputs[0] == "2":
        if len(inputs) == 1:
            return "CON Enter receiver's phone number"
        elif len(inputs) == 2:
            update_session(session, {"receiver_phone_number": inputs[1]})
            return "CON Enter Amount"
        elif len(inputs) == 3:
            update_session(session, {"amount": inputs[2]})
            return "CON Enter PIN"
        elif len(inputs) == 4:
            receiver = data.get("receiver")
            amount = float(data.get("amount"))
            pin = inputs[3]

            user = User.objects.get(phone_number=phone_number)
            account = Account.objects.get(user=user)

            if not account.check_pin(pin):
                clear_session(session)
                return "END Invalid PIN"

            success, message = handle_transfer(phone_number, receiver, amount)
            clear_session(session)

            if success:
                return f"END Transfer successful"
            else:
                return f"END failed: {message}"

    return "END Invalid Option!"
