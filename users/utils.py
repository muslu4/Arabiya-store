import json
import requests
from django.conf import settings
from .models import User


def send_push_notification(device_token, title, body, data=None):
    """
    Send push notification to a specific device token using Firebase FCM
    """
    if not device_token or not settings.FIREBASE_PROJECT_ID:
        return False
    
    try:
        # Firebase FCM endpoint
        url = f"https://fcm.googleapis.com/v1/projects/{settings.FIREBASE_PROJECT_ID}/messages:send"
        
        # Prepare the message
        message = {
            "message": {
                "token": device_token,
                "notification": {
                    "title": title,
                    "body": body
                },
                "data": data or {},
                "android": {
                    "notification": {
                        "click_action": "FLUTTER_NOTIFICATION_CLICK",
                        "sound": "default"
                    }
                },
                "apns": {
                    "payload": {
                        "aps": {
                            "sound": "default"
                        }
                    }
                }
            }
        }
        
        # Get access token (you'll need to implement this based on your Firebase setup)
        access_token = get_firebase_access_token()
        
        if not access_token:
            print("Failed to get Firebase access token")
            return False
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(message))
        
        if response.status_code == 200:
            print(f"Push notification sent successfully to {device_token}")
            return True
        else:
            print(f"Failed to send push notification: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return False


def send_push_to_admins(title, body, data=None):
    """
    Send push notification to all admin users
    """
    admin_users = User.objects.filter(
        is_admin=True,
        is_active=True,
        device_token__isnull=False
    ).exclude(device_token='')
    
    success_count = 0
    
    for admin in admin_users:
        if send_push_notification(admin.device_token, title, body, data):
            success_count += 1
    
    print(f"Sent push notifications to {success_count}/{admin_users.count()} admin users")
    return success_count


def send_push_to_user(user_id, title, body, data=None):
    """
    Send push notification to a specific user
    """
    try:
        user = User.objects.get(id=user_id, is_active=True)
        if user.device_token:
            return send_push_notification(user.device_token, title, body, data)
        return False
    except User.DoesNotExist:
        print(f"User with ID {user_id} not found")
        return False


def get_firebase_access_token():
    """
    Get Firebase access token for FCM
    This is a simplified version - in production, you should use Firebase Admin SDK
    """
    try:
        # If you have Firebase credentials file
        if settings.FIREBASE_CREDENTIALS_PATH:
            import firebase_admin
            from firebase_admin import credentials, messaging
            
            # Initialize Firebase Admin SDK if not already done
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
            
            # For this simplified version, we'll use a different approach
            # In production, use Firebase Admin SDK properly
            return "your-server-key-here"  # Replace with actual server key
        
        return None
        
    except Exception as e:
        print(f"Error getting Firebase access token: {e}")
        return None


def send_fcm_notification_simple(device_token, title, body, data=None):
    """
    Simple FCM notification using legacy server key (for development)
    Replace with proper Firebase Admin SDK in production
    """
    if not device_token:
        return False
    
    try:
        # Legacy FCM endpoint (for development only)
        url = "https://fcm.googleapis.com/fcm/send"
        
        payload = {
            "to": device_token,
            "notification": {
                "title": title,
                "body": body,
                "sound": "default"
            },
            "data": data or {}
        }
        
        headers = {
            "Authorization": "key=YOUR_SERVER_KEY_HERE",  # Replace with your server key
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success', 0) > 0:
                print(f"FCM notification sent successfully")
                return True
            else:
                print(f"FCM notification failed: {result}")
                return False
        else:
            print(f"FCM request failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending FCM notification: {e}")
        return False


def normalize_phone_number(phone):
    """
    Normalize phone number to international format
    """
    if not phone:
        return phone
    
    # Remove all non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone))
    
    # Handle Saudi Arabia numbers
    if len(digits_only) == 9 and digits_only.startswith('5'):
        return '966' + digits_only
    elif len(digits_only) == 10 and digits_only.startswith('05'):
        return '966' + digits_only[1:]
    elif len(digits_only) == 12 and digits_only.startswith('966'):
        return digits_only
    
    return digits_only


def validate_phone_number(phone):
    """
    Validate phone number format
    """
    if not phone:
        return False, "رقم الهاتف مطلوب"
    
    normalized = normalize_phone_number(phone)
    
    if len(normalized) < 9:
        return False, "رقم الهاتف قصير جداً"
    
    if len(normalized) > 15:
        return False, "رقم الهاتف طويل جداً"
    
    # Check if it's a valid Saudi number
    if normalized.startswith('966') and len(normalized) == 12:
        if not normalized[3:].startswith('5'):
            return False, "رقم الهاتف السعودي يجب أن يبدأ بـ 5"
    
    return True, "رقم الهاتف صحيح"