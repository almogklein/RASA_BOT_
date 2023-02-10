# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import io
import openai
import random
import requests
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker 
from rasa_sdk.executor import CollectingDispatcher


class ActionParseUserText(Action):
    """Rasa action to parse user text and return a response from OpenAI API"""

    def name(self) -> Text:
        return "action_parse_user_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        # Get the latest user text and intent
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        
        # Dispatch the response from OpenAI to the user
        dispatcher.utter_message(f'mes_inte {intent}: ' + str(user_text))
        dispatcher.utter_message('Chatgpt: ' + self.get_answers_from_chatgpt(intent, user_text))
        # dispatcher.utter_message('Google Sheets: ' + random.choice(self.get_answers_from_sheets(intent)))

        return []

    def get_answers_from_sheets(self, intent):

        # Connect to Google Sheets
        GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/< SHEET_URL >/export?format=csv&gid=0"
        s = requests.get(GOOGLE_SHEET_URL).content
        
        proxy_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

        # Filter the dataframe by the intent
        answers = proxy_df[proxy_df['Intent'] == intent]['Answer'].tolist()

        return answers

    def get_answers_from_chatgpt(self, intent, user_text):

        # OpenAI API Key
        openai.api_key = "API_KEY"

         # Use OpenAI API to get the response for the given user text and intent
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Return an answer for the text + {intent} combination: " + user_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        return response