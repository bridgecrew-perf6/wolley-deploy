import os
import datetime
from myapi.settings.base import BASE_DIR

import firebase_admin
from firebase_admin import credentials, messaging


# This registration token comes from the client FCM SDKs.
token_ella = "fMJXSBOp0ETivyjy9tkV0H:APA91bGmWVhUeAeiBeOtJ9_BxWUOHqY8W1Zq32DNZcamPdT-vYLax73EKfnJMgZSEZCoXOD1-VFPTzF9vBmDgSp5oW310mwvl3AX5em84z_LzQebunZD7MaW7O7e8OBMTtb7JYzRxTaQ"
token_alpha = "fPsZLMDhw0APtq0Qs0cojU:APA91bEk8gsecsW78VOV2y_3ayWHRo7uJkOd39fimv-THiLrWTJOuK3JnG4SkQzAG8rxzalTdEDuItwNaCGYACRLyIPq-jJ5BH-2mgTIdzkCidTPr2ctL6x_j7VDHlKpFHLE9aIIhlQZ"


def init_app():
    # firebase 관련
    cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


def send_to_firebase_cloud_messaging(registration_token):
    # See documentation on defining a message payload.
    apns = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(content_available=True)  # individual needs in the background notification part
        )
    )
    message = messaging.Message(
        # silent noti를 원한다면, 아래 notification 부분을 주석처리 하면 된다.
        notification=messaging.Notification(
            title='(test) title 입니다.',
            body='(test) u r so pretty girl~',
        ),
        apns=apns,
        token=registration_token,
    )
    response = messaging.send(message)

    # Response is a message ID string.
    print('Successfully sent message:', response)


def send_to_firebase_cloud_group_messaging(registration_tokens):
    # See documentation on defining a message payload.
    apns = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(content_available=True)  # individual needs in the background notification part
        )
    )
    message = messaging.MulticastMessage(
        # silent noti를 원한다면, 아래 notification 부분을 주석처리 하면 된다.
        notification=messaging.Notification(
            title='(test) title 입니다.',
            body='(test) u r so pretty girl~',
        ),
        apns=apns,
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    print(f"{response.success_count} messages were sent successfully.")


if __name__ == "__main__":
    init_app()

    print(datetime.datetime.today())
    tokens = [token_alpha, token_ella]

    # for tok in tokens:
    #     send_to_firebase_cloud_messaging(tok)
    send_to_firebase_cloud_group_messaging(tokens)
