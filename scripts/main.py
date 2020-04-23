from email_recognition import *
from email_rpa import *
from urllib import request, parse
import json
import numpy as np
import argparse

def get_slack_url():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slack_url', help='Slack bot url to send a message to', dest='slack_url')
    args = parser.parse_args()
    if args.slack_url == None:
        return ''
    return  args.slack_url

# Posting to a Slack channel
def send_message_to_slack(text, slack_url):
    if slack_url == '':
        return

    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request(slack_url,
            data=json_data.encode('ascii'),
            headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def build_notif_message(order_text, email_headline):
    return 'New order email: {}. Email: {}'.format(order_text, email_headline[:100] + '...')

if __name__ == '__main__' :
    with open("./email_info_issproject.json",'r') as load_f:
        email_info = json.load(load_f)

    account = email_info['email']
    password = email_info['password']
    slack_url = get_slack_url()
    print('Slack url is {}'.format(slack_url))

    model = OrderEmailRecognition()
    rpa = create_rpa_email(account, password)


    rpa.open_email()
    emails = rpa.extract_email_headlines(limit=14)
    count = 0
    for email in emails:
        item_xpath, doc, is_unread = email[0], email[1], email[2]
        print(doc)
        print(is_unread)
        if not is_unread:
            print('email has been read')
            continue
        if not model.isDocOrderNotification(doc):
            print('is not order email')
            continue
        raw_content = rpa.get_email_content(item_xpath, is_unread)
        order_text = model.extractOrderStatusRelatedText(raw_content)
        notif_message = build_notif_message(order_text, doc)
        print(notif_message)
        print('========================================')
        send_message_to_slack(notif_message, slack_url)
        count += 1
    print('Total email sent : {}'.format(count))
    rpa.close()
    print('Closed and finished the program')

