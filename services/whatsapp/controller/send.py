import requests
from services.whatsapp.models.wa_models import Buttons, List, Contact
import json
from app.utils.env import Env

def mark_as_read_message(message_id: str):
    requests.post(
        url=f'https://graph.facebook.com/v16.0/{Env.get_secure("WA_IDTEL")}/messages',
        headers={
            'Authorization': f'Bearer {Env.get_secure("WA_TOKEN")}',
            'Content-Type': 'application/json',
            'accept': 'application/json'
        },
        json={
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
    )

def send_controller(message: str | Buttons | List | Contact, to: str, message_id: str | None = None):
        body = {}
        if isinstance(message, str):
            body = {
                'to': to,
                'type': 'text',
                'text': {
                    'body': message,
                    'preview_url': 'true'
                },
                'recipient_type': 'individual',
                'messaging_product': 'whatsapp',
            }
        
        if isinstance(message, Buttons) or isinstance(message, List) or isinstance(message, Contact):
            body = message.get(to)

        if message_id:
            body['context'] = {
                'message_id': message_id
            }

        response = requests.post(
            url=f'https://graph.facebook.com/v16.0/{Env.get_secure("WA_IDTEL")}/messages',
            data=json.dumps(body),
            headers={
                'Authorization': f'Bearer {Env.get_secure("WA_TOKEN")}',
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        print(body)
        print(response.json())

        pass