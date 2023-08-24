
# import package
from decouple import config
import africastalking

# Initialize SDK
username = "vax"    # use 'sandbox' for development in the test environment
api_key = config('API_KEY')      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("Hello Mercy!", [config('mercy_phone')])
print(response)