import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (From, To, PlainTextContent, HtmlContent, Mail)

sendgrid_client = SendGridAPIClient(
    api_key=os.environ.get('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'))
from_email = From('manishadarling52@gmail.com')
to_email = To('manishadarling52@gmail.com')
subject = 'Sending with Twilio SendGrid is Fun'
plain_text_content = PlainTextContent(
    'and easy to do anywhere, even with Python'
)
html_content = HtmlContent(
    '<strong>and easy to do anywhere, even with Python</strong>'
)
message = Mail(from_email, to_email, subject, plain_text_content, html_content)
response = sendgrid_client.send(message=message)
print(response.status_code)
print(response.body)
print(response.headers)
