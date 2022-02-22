from firebase_admin import messaging


def send_to_firebase_cloud_messaging(registration_token, is_silent, msg_type, msg_title, msg_body):
    # See documentation on defining a message payload.
    apns = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(content_available=True, thread_id=msg_type)
        )
    )

    if is_silent:
        message = messaging.Message(
            apns=apns,
            token=registration_token,
        )
    else:
        message = messaging.Message(
            notification=messaging.Notification(
                title=msg_title,
                body=msg_body,
            ),
            apns=apns,
            token=registration_token,
        )
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


def send_to_firebase_cloud_group_messaging(registration_tokens, is_silent, msg_type, msg_title, msg_body):
    # See documentation on defining a message payload.

    apns = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(content_available=True, thread_id=msg_type)
        )
    )

    if is_silent:
        message = messaging.MulticastMessage(
            apns=apns,
            tokens=registration_tokens,
        )
    else:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=msg_title,
                body=msg_body,
            ),
            apns=apns,
            tokens=registration_tokens,
        )
    response = messaging.send_multicast(message)
    print(f"{response.success_count} messages were sent successfully.")


def func_to_schedule(appuser_tokens, is_silent, msg_type, msg_title, msg_body):
    try:
        send_to_firebase_cloud_group_messaging(appuser_tokens, is_silent, msg_type, msg_title, msg_body)
    except:
        print("There are no tokens")
