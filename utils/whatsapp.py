import requests
from django.conf import settings

# def send_whatsapp_message(to_number, message):
#     url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": to_number,
#         "type": "text",
#         "text": {"body": message}
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     return response.json()

# import requests
# import json

# def send_whatsapp_message(to_number, invitation_link):
#     # url = "https://graph.facebook.com/v22.0/<YOUR_PHONE_NUMBER_ID>/messages"
#     url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": "Bearer <YOUR_ACCESS_TOKEN>",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": str(to_number),
#         "type": "template",
#         "template": {
#             "name": "event_invitation",
#             "language": {"code": "en_US"},
#             "components": [
#                 {
#                     "type": "body",
#                     "parameters": [
#                         {"type": "text", "text": invitation_link}
#                     ]
#                 }
#             ]
#         }
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(payload))
#     return response.json()

# import requests
# import json


# def send_whatsapp_message(to_number, invitation_link):
#     url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
#         "Content-Type": "application/json",
#     }

#     # payload = {
#     #     "messaging_product": "whatsapp",
#     #     "to": to_number,
#     #     "type": "template",
#     #     "template": {
#     #         "name": "hello_world",
#     #         "language": {"code": "en_US"}
#     #     }
#     # }

#     # Optional: if you have a custom template with a variable link
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": to_number,
#         "type": "template",
#         "template": {
#             "name": "invitation_link",
#             "language": {"code": "en_US"},
#             "components": [
#                 {
#                     "type": "body",
#                     "parameters": [{"type": "text", "text": invitation_link}]
#                 }
#             ],
#         },
#     }
#     # payload = {
#     #     "messaging_product": "whatsapp",
#     #     "to": to_number,
#     #     "type": "template",
#     #     "template": {
#     #         "name": "invitation_link",
#     #         "language": {"code": "en_US"},
#     #         "components": [
#     #             {
#     #                 "type": "body",
#     #                 "parameters": [
#     #                     {"type": "text", "text": invitation_link}
#     #                 ]
#     #             }
#     #         ]
#     #     }
#     # }


#     response = requests.post(url, headers=headers, data=json.dumps(payload))
#     return response.json()

import requests
import json


def send_whatsapp_message(to_number, guest_name, event_name, event_date, invitation_link):
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    
    payload = {
        "messaging_product": "whatsapp",
        "to": str(to_number),
        "type": "template",
        "template": {
            "name": "invitation_link",
            # "language": {"code": "en"},
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": guest_name},
                        {"type": "text", "text": event_name},
                        {"type": "text", "text": event_date},
                        {"type": "text", "text": invitation_link},
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(json.dumps(payload, indent=2))

    return response.json()
