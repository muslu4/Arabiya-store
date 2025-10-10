from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
        if cred_path:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")

def send_push_to_user(user, title, body, data=None):
    """
    Send a push notification to a specific user
    """
    try:
        # Get user's FCM token
        if hasattr(user, 'fcm_token') and user.fcm_token:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=user.fcm_token
            )

            # Send the message
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            return True
        return False
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return False

def send_push_to_admins(title, body, data=None):
    """
    Send a push notification to all admin users
    """
    from .models import User

    try:
        # Get all admin users with FCM tokens
        admins = User.objects.filter(is_staff=True, fcm_token__isnull=False)

        # Create a multicast message
        tokens = [admin.fcm_token for admin in admins]

        if not tokens:
            return False

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},
            tokens=tokens
        )

        # Send the message
        response = messaging.send_multicast(message)
        print(f"Successfully sent multicast message: {response}")
        return True
    except Exception as e:
        print(f"Error sending push notification to admins: {e}")
        return False
