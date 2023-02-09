from sendgrid import SendGridAPIClient, Mail

constant = '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'
sg = SendGridAPIClient(constant)
subject = 'hello'
content = 'hi'
message = Mail(
    from_email=('manishadarling52@gmail.com', 'Hello'),
    to_emails=['harini@gmail.com', 'monisha@gmail.com'],
    subject=subject,
    html_content=content)
response = sg.send(message)
print(response.status_code)
print(response.body)
print(response.headers)
