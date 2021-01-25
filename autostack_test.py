from slack import WebClient
from autostack import AutoStackBot
import os

# Create a slack client
# os.environ.get("SLACK_TOKEN")
slack_web_client = WebClient(token=os.environ.get("SLACK_APP_TOKEN"))

# Get a new CoinBot
auto_stack = AutoStackBot("#slack-bots")

# Get the onboarding message payload
message = auto_stack.generate_message_payload('value error')

# print(message)

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)
