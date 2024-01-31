from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "from South Canteen"
sender = {"name":"Sendinblue","email":"it1566.03.sc@gmail.com"}
replyTo = {"name":"Sendinblue","email":"it1566.03.sc@gmail.com"}
html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
to = [{"email":"kohkady23@gmail.com","name":"Jane Doe"}]
params = {"parameter":"My param value","subject":"First transactional email"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)