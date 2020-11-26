# send message through twilio
# make sure you install twilio by running `pip install twilio` before running the file
    # for some reason, running this file works on my terminal but not through the terminal in VSCode...that may or may not be the case for you

from twilio.rest import Client

# account_sid, auth_token, and from_ values are from Jiin's free twilio account
account_sid = "ACac37375f5a3dfe6441f409bca3991a65"
auth_token = "9c2286b24b2a3d15c9f39130298d5aa9"
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="insert phone number here, including the area code", # This is the number that the message will be sent to. Change it to your phone number to test it out
    from_="+12184266434",
    body="Submit your feedback for today's lesson here: https://forms.gle/kBKVBfA2YyQ8ft3b6"
)

print(message.sid)