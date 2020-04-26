## SECTION 1 : PROJECT TITLE
## Order Email Notification

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT

The evolution of artificial intelligence has become a hot topic in recent years. More companies are in the wave of embracing the recent technology practice called robotic process automation (RPA) to streamline certain processes and operations. With RPA, automation of mundane rules-based business processes is easily achieved. This has enabled business users to devote more time to higher-value work that would require human decision. By integrating the RPA with the knowledge of intelligent automation (IA) via Machine Learning (ML) and Artificial Intelligence (AI) tools, which is also known as Intelligent Process Automation (IPA), the models could be trained to replace mundane business process and at the same time make certain decision based on trained data. This convergence of technologies produces automation capabilities which has dramatically elevated competitive advantages for the companies.

One of the leaders in the IPA sector is UiPath. UiPath has amplified the power of their RPA technology by using artificial intelligence (AI) to create IPA solutions in three ways - unattended robotics, advanced computer vision and integration with third party cognitive services from Microsoft, ABBYY, Google and IBM. In the continuous development of the IPA, UiPath is looking to the enhanced version of IPA which offers more Natural Language Processing and Machine Learning services on Cloud in the next few patches.

In this project, by applying the knowledge of IPA, we have looked into automate a process that could eliminate the tedious process in our daily life. Online shopping has been the hot trend following global blooming of internet usage. Consumers can search for a product by surfing the website of the retailer directly or by searching among alternative vendors using a shopping search engine. Different online shopping platforms offer different kinds of products as well as pricing strategies, which depends on the vendors. Some of the famous online shopping platforms in Singapore are Lazada, Shopee and Zalora. However, while we tend to buy a lot of stuff from different online shopping platforms, tracing the status of an order could become an issue. Most of the online shopping platforms would send a notification email to the user upon confirmation of order, or updating of the order status. In order to ease tracing of order status within the chunk of emails, we proudly present the “Order Email Notification” system which would help us retrieve relevant order email and provide an update through Skype. The details would be shared in the subsequent sections.


---
## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Lee Boon Kien | A0195175W | Video Presentation, Report Writing, RPA module | e0384806@u.nus.edu |
| Raymond Djajalaksana| A0195381X | Local AI Building, Report Writing, RPA module | e0385012@u.nus.edu |


---
## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[![Order Email Notification](http://img.youtube.com/vi/juZ6AsPIpkI/0.jpg)](https://www.youtube.com/watch?v=juZ6AsPIpkI)

---
## SECTION 5 : USER GUIDE
### Pre-Requisite

Please prepare below items before we can start with the application:
- Valid hotmail/outlook/gmail (email and password)
- For gmail, please prepare stackoverflow account created with gmail sign in. We will use this as a way to log in to gmail.
- Valid Slack bot url for notification purpose

### Installment

using pip
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

using anaconda
```
conda create -n isy5005_ipa python=3.7.1
conda activate isy5005_ipa
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Usage

```
python main.py --slack_url your_slack_bot_url
```

---
## SECTION 6 : PROJECT REPORT / PAPER
`Order_Email_Notification.pdf` : <https://github.com/raycap/isy5005_ipa/report/isy5005_IPA_Group_8.pdf>

---