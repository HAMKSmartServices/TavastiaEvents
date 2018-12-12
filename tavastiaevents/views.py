from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from django.views.decorators.csrf import csrf_exempt

from events.models import Event

from django.core.mail import send_mail

from django.conf import settings


MESSAGE_CODES = (
        (100, 'Error'),
        (200, 'Report'),
        (300, 'PIN'),
    )

@csrf_exempt
def message_event(request):
    if request.method == 'POST':

        event_to_report = request.POST.get('event_id', None)
        message_code = request.POST.get('message_code', None)
        message = request.POST.get('message', None)

        if message is not None:
            message = str(message)
            if len(message) > 300:
                responseData = {
                    'message': "Message length can't exceed 300 characters"
                }
                return JsonResponse(responseData, status=400)


        if event_to_report == None or message_code == None:
            responseData = {
                'required': 'event_id and message_code must be suplied with the report'
            }
            return JsonResponse(responseData, status=400)

        sender_email = settings.EMAIL_HOST_USER
        email_subject = ''
        email_message = ''
        email_to = []

        try:
            event = Event.objects.get(id=event_to_report)
        except Event.DoesNotExist:
            event = None
            responseData = {
                'event_id': 'Event with that id was not found'
            }
            return JsonResponse(responseData, status=400)

        if int(message_code) == 100:
            email_subject = 'Tavastia Events: Tapahtumasi tiedoissa mahdollinen virhe'
            email_message = 'Tapahtuman tiedoissa on mahdollisesti virhe. Pyydämme tarkistamaan tiedot.\nTapahtuman nimi {0}\nTapahtuman id: {1}\n'.format(event.id, event.name)
            if message != '' and message != None:
                email_message += '\nIlmoituksen mukana lähetettiin seuraava lisätieto: \n' 
                email_message += message
            email_to = [event.provider_email, 'admin@tavastiaevents.fi']

        elif int(message_code) == 200:
            email_subject = 'Tavastia Events: Tapahtuma ilmoitettu'
            email_message = 'Tapahtumasta {0}: {1} on tehty ilmoitus käyttöehtojen vastaisena\n'.format(event.id, event.name)
            if message != '' and message != None:
                email_message += '\nIlmoituksen mukana lähetettiin seuraava lisätieto: \n' 
                email_message += message

            email_to = ['admin@tavastiaevents.fi']
        
        elif int(message_code) == 300:
            email_subject = 'Tavastia Events: Tapahtumaan liittyvä PIN-koodi'
            email_message = 'Tässä pyytämäsi tapahtumaan {0}: {1} liitetty PIN-koodi. \nPIN-koodi: {2}'.format(event.id, event.name, event.pin)

            email_to = [event.provider_email, 'admin@tavastiaevents.fi']

        else:
            responseData = {
                'message_code': 'Message code was not found on the server'
            }
            return JsonResponse(responseData, status=400)

        if email_message != '':
            send_mail(email_subject, email_message, sender_email, email_to, fail_silently=False)
            responseData = {
                'message_sent': 'Successful'
            }
            return JsonResponse(responseData)
        else:
            responseData = {
                'server_error': 'Error occurred on server. Please try again'
            }
            return JsonResponse(responseData, status=500)

    else:
        raise PermissionDenied