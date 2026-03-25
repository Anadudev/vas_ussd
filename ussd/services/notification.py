import logging


logger = logging.getLogger(__name__)

def send_sms(phone_number: str, message: str):
    """ Simulate sending an SMS to a phone number """
    logger.info(f"SMS sent to {phone_number}: {message}")