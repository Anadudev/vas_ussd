from ussd.models import UssdSession


def get_or_create_session(session_id: str, phone_number: str) -> UssdSession:
    """ Get or create a new user USSD session. """
    session, created = UssdSession.objects.get_or_create(
        session_id=session_id,
        defaults={"phone_number": phone_number},
    )
    return session


def update_session(session: UssdSession, data: dict) -> None:
    """ update user's session """
    session.data.update(data)
    session.save()


def clear_session(session: UssdSession) -> None:
    """ clear user's session """
    session.is_active = False
    session.save()
