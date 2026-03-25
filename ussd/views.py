from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from ussd.services.session_manager import get_or_create_session
from ussd.services.ussd_handler import ussd_handler


@csrf_exempt
def ussd_callback(request: HttpRequest) -> HttpResponse:
    """ Handle USSD callbacks requests from client """
    session_id = request.POST.get("sessionId")
    phone_number = request.POST.get("phoneNumber")
    text = request.POST.get("text", "")

    print(f"session_id:{session_id}, phone_number:{phone_number}, text:{text}")

    session = get_or_create_session(session_id, phone_number)
    response = ussd_handler(session, text, phone_number)

    return HttpResponse(response,content_type="text/plain")