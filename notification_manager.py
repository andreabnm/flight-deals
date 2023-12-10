from twilio.rest import Client

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, fromNo, toNo, text):
        message = self.client.messages \
            .create(
            body=text,
            from_=fromNo,
            to=toNo
        )
