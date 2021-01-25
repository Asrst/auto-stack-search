import os
import logging
from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from autostack import AutoStackBot
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
import requests

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_APP_TOKEN"))

@app.route('/', methods=['GET'])
def home():
    return 'Hi, App is Running..!'


@app.route('/autostack', methods=['POST'])
def slash_command():
    # The parameters included in a slash command request (with example values):
    #   token=gIkuvaNzQIHg97ATvDxqgjtO
    #   team_id=T0001
    #   team_domain=example
    #   channel_id=C2147483705
    #   channel_name=test
    #   user_id=U2147483697
    #   user_name=Steve
    #   command=/weather
    #   text=94070
    #   response_url=https://hooks.slack.com/commands/1234/5678

    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', '')
    channel_id = request.form.get("channel")
    response_url = request.form.get("response_url")
    # Validate the request parameters
    # if not token:  # or some other failure condition
    #     abort(400)
    auto_stack = AutoStackBot(channel_id)
    # Get the onboarding message payload
    payload = auto_stack.generate_message_payload(text)
    # r = requests.post(response_url, json=payload)
    return payload


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "search" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel
        auto_stack = AutoStackBot(channel_id)

        # Get the onboarding message payload
        message = auto_stack.generate_message_payload(text)

        # Post the onboarding message in Slack
        slack_web_client.chat_postMessage(**message)

        return {}

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(threaded = True, port=5000)