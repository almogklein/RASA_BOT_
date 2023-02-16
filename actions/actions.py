# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import io
import os
import openai
import random
import requests
import pandas as pd
from dotenv import load_dotenv
from rasa_sdk import Action, Tracker 
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher


class Simple_Action(Action):

    """Parse user text and pulls a corresponding answer 
    from google sheet & OpenAI API, based on the intent and entities."""

    def name(self) -> Text:
        return "simple_action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")
        
        return []


class Simple_Google_sheet_Action(Action):

    """Rasa action to parse user text and pulls a corresponding answer 
    from google sheet based on the intent and entities."""

    def name(self) -> Text:
        return "simple_google_sheet_action" 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        # Get the latest user text and intent
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        # entities = tracker.latest_message.get('entities')
        
        # Dispatch the response from OpenAI to the user
        dispatcher.utter_message(f'mes_inte:{intent}\n')
        dispatcher.utter_message('Google Sheets: ' + str(self.get_answers_from_sheets(intent)))

        return []
    
    def get_answers_from_sheets(self, intent):

        # Connect to Google Sheets
        load_dotenv()
        sheet_url = os.getenv("SHEET_URL")

        GOOGLE_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{sheet_url}/export?format=csv&gid=0"
        s = requests.get(GOOGLE_SHEET_URL).content
        
        # Read the contents of the URL as a CSV file and store it in a dataframe
        proxy_df = pd.read_csv(io.StringIO(s.decode('utf-8')))        # Filter the dataframe by the intent column and retrieve the answer list
        
        answer = proxy_df[proxy_df['Intent'] == intent]['Answer'].tolist()
        # answer = random.choice(answers)

        # Return the answer list
        return answer


class Simple_ChatGPT_Action(Action):

    """Parse user text and pulls a corresponding answer 
    From OpenAI ChatGPT API, based on the intent and entities."""

    def name(self) -> Text:
        return "simple_chatgpt_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        # Get the latest user text and intent
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        entities = tracker.latest_message.get('entities')
        
        # Dispatch the response from OpenAI to the user
        dispatcher.utter_message(f'mes_inte:{intent}\n')
        dispatcher.utter_message('Chatgpt: ' + self.get_answers_from_chatgpt(intent, user_text))

        return []

    def get_answers_from_chatgpt(self, intent, user_text):

        # OpenAI API Key
        load_dotenv()
        openai.api_key = os.getenv("GPT_API_KEY")

        # Use OpenAI API to get the response for the given user text and intent
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Return an answer for the text + {intent} combination: " + user_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        # Return the response from OpenAI
        return response