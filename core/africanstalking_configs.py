from decouple import config


import africastalking

username = "vax"
api_key = config('API_KEY')
africastalking.initialize(username, api_key)

sms = africastalking.SMS