from email_recognition import *
from email_rpa import *
from urllib import request, parse
import json
import numpy as np
# Posting to a Slack channel
def send_message_to_slack(text):
	post = {"text": "{0}".format(text)}
	try:
		json_data = json.dumps(post)
		req = request.Request("https://hooks.slack.com/services/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",
			data=json_data.encode('ascii'),
			headers={'Content-Type': 'application/json'})
		resp = request.urlopen(req)
	except Exception as em:
		print("EXCEPTION: " + str(em))

def build_notif_message(email_headline):
	return 'New order email has arrived. Email: {}'.format(email_headline[:100] + '...')

if __name__ == '__main__' :
    with open("./email_info_issproject.json",'r') as load_f:
        email_info = json.load(load_f)
    account = email_info['email']
    password = email_info['password']
    model = OrderEmailRecognition()
    rpa = create_rpa_email(account, password)

    emails = rpa.start_get_emails()
    for email in emails:
        doc = email[1]
        if not model.isDocOrderNotification(doc):
            print('email {} is not order notification'.format(doc[:100]))
            continue
#        print('email {} is order notification'.format(doc))
        notif_message = build_notif_message(doc)
        send_message_to_slack(notif_message)
    rpa.close()

