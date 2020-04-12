from email_recognition import *
from email_rpa import *
from urllib import request, parse
	
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

 if __name__ == '__main__':
 	account = ''
 	password = ''
 	model = OrderEmailRecognition()
 	rpa = create_rpa_email(account, password)

 	emails = rpa.start_get_emails()
 	for email in emails:
 		doc = emails[1]
 		if not model.isDocOrderNotification(doc):
 			continue
		print('email {} is order notification'.format(doc))
		notif_message = build_notif_message(doc)
		send_message_to_slack(notif_message)
	rpa.close()

