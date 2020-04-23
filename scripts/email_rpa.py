import tagui as t
import numpy as np


class OutlookRPA:
    def __init__(self, account, password):
        self.account = account
        self.password = password

    def open_email(self):
        t.init(visual_automation = False)
        self.login()
    
    def login(self):
        t.url('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1586073207&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d6590c65e-2e3f-b1ed-bda9-2c5e901a9000&id=292841&aadredir=1&whr=outlook.sg&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015')
        t.wait(1)
        type_into('//*[@type="email"]', self.account + '[enter]')
        t.wait(1)
        type_into('//*[@name="passwd"]', self.password + '[enter]')

    def extract_email_headlines(self, limit=100):
        list_item = []
        listbox_xpath = '//div[@role="listbox"]'
        
        if limit == 0 :
            limit = 1000
        for i in range(1, limit+1):
            item_xpath = '(' + listbox_xpath + '//div[@role="option"])[{}]'.format(i)
            if not wait_element(item_xpath):
                print('email {} is not present'.format(i))
                break
            hover('(//div[contains(@class,"showHoverActionsOnHover")])[{}]'.format(i))
            email_headline = read(item_xpath + '/@aria-label')
            email_classes = read('(//div[contains(@class,"showHoverActionsOnHover")])[{}]/@class'.format(i))
            email_unread = is_email_unread(email_classes)
            list_item.append([item_xpath, email_headline, email_unread])
        return list_item

    def search_keyword(self, keyword):
        clear_button  = '//button[@aria-label="Exit Search"]'
        search_button = '//button[@aria-label="Search"]'
        if t.present(clear_button):
            click(clear_button)
            type_into('//input[contains(@aria-label, "Search")]', keyword )
            click(search_button)
            
    def get_email_content(self,item_xpath, is_unread):
        click(item_xpath)
        raw_text = read('//div[@class="wide-content-host"]')
        if is_unread:
            self.mark_as_unread()
        self.back_to_homelist()
        return raw_text
    
    # mark email as unread in home 
    def mark_as_unread(self):
        more_action_xpath = '//button[@aria-label="More mail actions"]'
        mark_as_unread_xpath = '//button[@name="Mark as unread"]'
        mark_as_read_xpath = '//button[@name="Mark as read"]'
        click(more_action_xpath)
        if present(mark_as_read_xpath, timeout=3):
            click(mark_as_read_xpath)
            t.wait(1)
            click(more_action_xpath)
        if present(mark_as_unread_xpath, timeout=3):
            click(mark_as_unread_xpath)            
        t.wait(1)
        
    # this is go back from content to homelist
    def back_to_homelist(self):
        click('//button[@aria-label="Close"]')
        t.wait(1)
        
    def close(self):
        t.close()

class GmailRPA:
    def __init__(self, account, password):
        self.account = account
        self.password = password

    def open_email(self):
        t.init(visual_automation = False)
        self.login()

    def login(self):
        ## TODO ::
        return

    def extract_email_headlines(self, limit=100):
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
            email_headline = read(item_xpath)
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
        print('using GmailRPA')
        return GmailRPA(account, password)
    if 'outlook' in account.split('@')[1] or 'hotmail' in account.split('@')[1]:
        print('using OutlookRPA')
        return OutlookRPA(account, password)

    print('email provider is not recognized. Defaulting ot outlook rpa')
    return OutlookRPA(account, password)


def type_into(xpath, type_cmd):
    wait_element(xpath)
    t.type(xpath, type_cmd)

def click(xpath):
    wait_element(xpath)
    t.click(xpath)

def present(xpath, timeout=7):
    return wait_element(xpath, timeout=timeout)

def read(xpath):
    wait_element(xpath)
    return t.read(xpath)

def hover(xpath):
    wait_element(xpath)
    return t.hover(xpath)

def wait_element(xpath, timeout=7):
    for i in range(timeout):
        if t.present(xpath):
            return True
        t.wait(1)
    return False

def is_email_unread(class_str):
    class_n = class_str.split('showHoverActionsOnHover')
    if len(class_n) <2:
        return False
    if class_n[1] != '' :
        return True
    return False