import firebase_admin
from firebase_admin import messaging, credentials


def send_to_firebase_cloud_messaging():
    # This registration token comes from the client FCM SDKs.
    registration_token = "fMJXSBOp0ETivyjy9tkV0H:APA91bGmWVhUeAeiBeOtJ9_BxWUOHqY8W1Zq32DNZcamPdT-vYLax73EKfnJMgZSEZCoXOD1-VFPTzF9vBmDgSp5oW310mwvl3AX5em84z_LzQebunZD7MaW7O7e8OBMTtb7JYzRxTaQ"

    # See documentation on defining a message payload.
    message = messaging.Message(

        # silent noti를 원한다면, 아래 notification 부분을 주석처리 하면 된다.
        notification=messaging.Notification(
            title='안녕하세요 타이틀 입니다',
            body='안녕하세요 메세지 입니다',
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


if __name__ == "__main__":
    import os
    from myapi.settings import BASE_DIR

    send_to_firebase_cloud_messaging()
