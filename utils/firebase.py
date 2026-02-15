# # homofix_app/firebase_init.py
# import firebase_admin
# from firebase_admin import credentials
# from django.conf import settings

import firebase_admin
from firebase_admin import credentials, messaging
import os

from django.conf import settings

# cred_path = os.path.join(settings.BASE_DIR, 'homofix-app-firebase-adminsdk-fbsvc-1ff7eab745.json')
cred_path = os.path.join(settings.BASE_DIR, 'homofixexpert-firebase-adminsdk-fbsvc-1321aada02.json')


# Initialize only once
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path )
    firebase_admin.initialize_app(cred)


# utils/firebase.py (continue)

def send_push_notification(token, title, body, data=None):
    """
    Send FCM notification to a device using its token.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {},  # Optional key-value data
    )

    try:
        response = messaging.send(message)
        return {'success': True, 'response': response}
    except Exception as e:
        return {'success': False, 'error': str(e)}

