# send a message through twilio

# make sure you install twilio by running `pip install twilio` before running the file
    # for some reason, running this file works on my terminal but not through the terminal in VSCode...that may or may not be the case for you

from twilio.rest import Client

# account_sid, auth_token, and from_ values are from your free twilio account
# for security reasons, I (Jiin) can't leave my account sid, auth token, and twilio number on here :( So you'll have to make your own free twilio account. It's super simple to do: 
    # 1. create an account here: https://www.twilio.com/try-twilio?_ga=2.182390127.916037802.1606343073-1380573367.1606343073
    # 2. Find the account SID and auth token here and generate a Twilio phone number here as well: https://www.twilio.com/console
# after testing, make sure you remove any info related to your account before pushing to the repo

account_sid = "INSERT_ACCOUNT_SID"
auth_token = "INSERT_AUTH_TOKEN"
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="INSERT_RECEIVER_PHONE_NUMBER", # This is the number that the message will be sent to. Change it to your phone number to test it out
    from_="INSERT_TWILIO_PHONE_NUMBER",
    body="Submit your feedback for today's lesson here: https://forms.gle/kBKVBfA2YyQ8ft3b6" # this is a sample form that I (Jiin) created
)

print(message.sid)