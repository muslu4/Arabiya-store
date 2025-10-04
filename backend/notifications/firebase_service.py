import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

# Initialize Firebase
def initialize_firebase():
    try:
        if not firebase_admin._apps:
            # اقرأ JSON من Environment Variable
            firebase_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
            if not firebase_json:
                print("Firebase credentials JSON not found in environment")
                return False

            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully")
        else:
            print("Firebase already initialized")
        return True
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return False
# Send notification to a specific device
def send_notification_to_device(token, title, body, data=None):
    try:
        # Create a message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=token,
        )

        # Send the message
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
        return True
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False

# Send notification to a topic
def send_notification_to_topic(topic, title, body, data=None):
    try:
        # Create a message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            topic=topic,
        )

        # Send the message
        response = messaging.send(message)
        print(f"Successfully sent message to topic: {response}")
        return True
    except Exception as e:
        print(f"Error sending notification to topic: {str(e)}")
        return False

# Subscribe a device to a topic
def subscribe_to_topic(tokens, topic):
    try:
        # Subscribe the devices to the topic
        response = messaging.subscribe_to_topic(tokens, topic)
        print(f"Successfully subscribed to topic: {response}")
        return True
    except Exception as e:
        print(f"Error subscribing to topic: {str(e)}")
        return False
