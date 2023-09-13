"""This program will make calls to the chatgpt api. It will pass gpt a user input that briefly describes 
the user's organization and selling points. It will then ask gpt to suggest some words that the user 
might want to spell using the last 4-7 digits of their 1-800 number.
"""

import requests
import json
import re
from confidential import chatgpt_api_key

"""This class calls the OpenAI API for ChatGPT."""
class APICall():
    # default user message is provided for ease of testing.
    def __init__(self, user_message="Faxi is the fastest taxi operation in town. We'll get you there with your hair blown back!"):
        self.API_KEY = chatgpt_api_key
        self.user_message = user_message
        self.url = "https://api.openai.com/v1/chat/completions"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_KEY}"
        }

        self.data = {
            "model": "gpt-3.5-turbo",
            # The message wraps the user's description of their organization. It is designed to solicit 
            # a list of suggestions in the format of a python list. This format, in turn, allows the 
            # regex pattern to recognize the suggestions because they are between quotes.
            "messages": [{"role": "user", "content": f"A colleague of mine is thinking about getting a 1-800 number. Here is their description of their organization: '{self.user_message}' My colleague wants help coming up with words or phrases that they can spell using the last 4-7 digits of their 1-800 number. Will you please help me by coming up with 20 words that they could use? It would be helpful if you wrote the words in the form of a python list of strings."}],
            "temperature": 0.7
        }

    # This function makes the call to the API and returns the list of suggestion strings from the response
    def prepare_suggestions(self):
        self.response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data), timeout=30)

        if self.response.status_code == 200:
            self.response_data = self.response.json()
            self.generated_text = self.response_data['choices'][0]['message']['content']    # select the content of the response (instead of the metadata)
            suggestion_list = self.match_list(self.generated_text)      # make a list of the suggested words that are in quotation marks
            return suggestion_list
        else:
            return f"Error: {self.response.status_code}\n{self.response.text}"

    # This function recognizes suggested words inside of the response content by seeking words in quotation marks
    def match_list(self, text):
        list_regex = re.compile(r"""["'](\w*)["'],""")
        mo = list_regex.findall(text, 1)
        return mo

if __name__ == "__main__":
    main_instance = APICall()

# TESTING
# print(main_instance.match_list("""
#     Sure! Here is a list of 20 words or phrases that can be spelled using the last 4-7 digits of a 1-800 number:

# ```python
# words = [
#     "FAST",
#     "TAXI",
#     "BLOW",
#     "HAIR",
#     "BACK",
#     "FAXI",
#     "TOWN",
#     "FAIR",
#     "RIDE",
#     "CALL",
#     "CAB",
#     "DRIVE",
#     "LIMO",
#     "CARS",
#     "MOVE",
#     "JUMP",
#     "RUSH",
#     "SPEED",
# """))