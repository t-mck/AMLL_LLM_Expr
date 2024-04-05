import textwrap

import yaml
import google.generativeai as genai

from IPython.display import display, Markdown

# This key is gitignored, because I didn't want to put it on the Internet. Find in Box.
with open('gemini-api.yaml') as rf:
    API_KEY = yaml.safe_load(rf)['api-key']

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
    return Markdown(textwrap.indent(text.replace('•', '  *'), '> ', predicate=lambda _: True))

class Chat:
    '''
    Chat object, based on message structure. Defaults to instantiated Gemini Pro model.
    '''
    def __init__(self, model=model):
        self.model = model
        self.chat = self.model.start_chat(history=[])

    def get_history(self):
        '''
        Function to return single chat response from initialized Gemini Pro instance.

        Args:
        None.

        Returns:
        list of dict: parts (returned messages), role (user/model).
        '''
        return self.chat.history
    
    def send_message(self, msg):
        '''
        Function to return single chat response from initialized Gemini Pro instance.

        Args:
        msg (str): Message to send.

        Returns:
        (str): Returned message.
        '''
        return self.chat.send_message(msg)

def single_response(msg: str):
    '''
    Function to return single chat response from initialized Gemini Pro instance.

    Args:
    msg (str): Message to send.

    Returns:
    (str): Returned message.
    '''
    return model.generate_content(msg)