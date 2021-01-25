# import the random library to help us generate the random numbers
import random
import requests
import ast

# Create the CoinBot Class
class AutoStackBot:

    # Create a constant that contains the default text for the message
    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*I got the following..!*",
            },
            }

    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self, channel):
        self.channel = channel

    # Generate a random number to simulate flipping a coin. Then return the
    # crafted slack payload with the coin flip message.
    def _search_stack(self, msg_txt):

        stack_api = 'https://api.stackexchange.com/2.2/search/advanced'

        param_dict = {'title':msg_txt,'tagged':'python', 
            'order': 'desc', 'sort': 'relevance', 
            'accepted': True, 'site': 'stackoverflow'}

        try:
            r = requests.get(stack_api, params = param_dict)
            r_json = r.json()['items']
        except Exception as e:
            print(e)
            r_json = {}

        response_text = ""
        for d in r_json[:5]:
            # d = ast.literal_eval(d)
            t = "<{}|{}>".format(d['link'], d['title'])
            response_text += t
            response_text += '\n'

        return {"type": "section", 
                "text": {"type": "mrkdwn", "text": response_text}},

    # Craft and return the entire message payload as a dictionary.
    def generate_message_payload(self, msg_txt):
        return {
            "channel": self.channel,
            "blocks": [
                self.MESSAGE_BLOCK,
                *self._search_stack(msg_txt),
            ],
        }
