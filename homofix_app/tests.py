# from django.test import TestCase
# import requests

# # import geopy
# # Create your tests here.

# import urllib.parse
# username = "TRYGON"
# apikey = "E705A-DFEDC"
# apirequest="Text"
# sender ="TRYGON"
# mobile="9310140032"
# message="Dear armaan 123485 is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
# TemplateID="1707162192151162124"
# # url = f"http://message.trygon.in/sms-panel/api/http/index.php?username={username}&apikey={apikey}&apirequest={apirequest}&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1707162192151162124&format=JSON"
# url = f"https://sms.webtextsolution.com/sms-panel/api/http/index.php?username=TRYGON&apikey=E705A-DFEDC&apirequest=Text&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1707162192151162124&format=JSON"

# response = requests.get(url)
# print("ddddddddd",response)

# if response.ok:
#     print("SMS message sent successfully")
# else:
#     print("Error sending SMS message")


# # auth_key = "IQkJfqxEfD5l3qCu"
# # sender_id = "TRYGON"
# # route = 2
# # number = "9973884727"
# # message = "Dear armuu 1005 is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
# # template_id = "1707162192151162124"
# # url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
# # response = requests.get(url)
# # print("ddddddddd",response)

# # if response.ok:
# #     print("SMS message sent successfully")
# # else:
# #     print("Error sending SMS message")

order = "20240401"
print(order[-2])