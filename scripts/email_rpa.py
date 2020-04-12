import tagui as t
import numpy as np


class OutlookRPA:
	def __init__(self, account, password):
		self.account = account
		self.password = password

	def start_get_emails():
		t.init(visual_automation = False)
		self.login()
		return self.extract_email_headlines()

	def login(self):
		t.url('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1586073207&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d6590c65e-2e3f-b1ed-bda9-2c5e901a9000&id=292841&aadredir=1&whr=outlook.sg&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015')
    	type_into('//*[@type="email"]', self.account + '[enter]')
    	type_into('//*[@name="passwd"]', self.password + '[enter]')

    def extract_email_headlines(limit=100):
		list_item = []
		listbox_xpath = '//div[@role="listbox"]'
		if limit == 0 :
			limit = 1000
		for i in range(1, limit+1):
			item_xpath = '(' + listbox_xpath + '//div[@role="option"])[{}]'.format(i)
			if not present(item_xpath):
				print('email {} is not present'.format(i))
				break
			email_id = t.read(item_xpath + '/@data-convid')
			email_headline = t.read(item_xpath + '/@aria-label')
			list_item.append((email_id, email_headline))
		return np.array(list_item)

	def search_keyword(self, keyword):
		clear_button  = '//button[@aria-label="Exit Search"]'
		search_button = '//button[@aria-label="Search"]'
		if t.present(clear_button):
			click(clear_button)
			type_into('//input[contains(@aria-label, "Search")]', keyword )
			click(search_button)
	def close(self):
		t.close()

class GmailRPA:
	def __init__(self, account, password):
		self.account = account
		self.password = password

	def start_get_emails():
		t.init(visual_automation = False)
		self.login()
		return self.extract_email_headlines()
	
	def login(self):
		## TODO ::
		return

	def extract_email_headlines():
		list_item = []
		listbox_xpath = '(//table[@class="F cf zt"])[2]'
		if limit == 0 :
			limit = 1000
		i = 1
		while len(list_item) < limit:
			item_xpath = '(' + listbox_xpath + '//tr)[{}]//td[@class="xY a4W"]'.format(i)
			if not present(item_xpath):
				older_button = '//div[@data-tooltip="Older"]'
				click(older_button)
				i = 1
				continue
			email_id = ""
			email_headline = clean_raw_text(read(item_xpath))
			list_item.append((email_id, email_headline))
			i += 1
		return np.array(list_item)

	def close(self):
		t.close()



## UTILS

def create_rpa_email(account, password):
	if len(account.split('@')) != 2:
		print('error email does not have @')
	if 'gmail' in account.split('@')[1]:
		return GmailRPA(account, password)
	if 'outlook' in account.split('@')[1] or 'hotmail' in account.split('@')[1]:
		return OutlookRPA(account, password)

	print('email provider is not recognized. Defaulting ot outlook rpa')
	return OutlookRPA(account, password)


def type_into(xpath, type_cmd):
	wait_element(xpath)
	t.type(xpath, type_cmd)

def click(xpath):
	wait_element(xpath)
	t.click(xpath)

def present(xpath):
	return wait_element(xpath)

def read(xpath):
	wait_element(xpath)
	return t.read(xpath)

def wait_element(xpath):
	for i in range(10):
		if t.present(xpath):
			return True
		t.wait(1)
		return False

def get_email_content(i):
	listbox_xpath = '//div[@role="listbox"]'
	item_xpath = '(' + listbox_xpath + '//div[@role="option"])[{}]'.format(i)
	click(item_xpath)
	return clean_raw_text(read('//div[@class="rps_25d6"]'))