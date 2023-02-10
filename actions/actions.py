# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker 
from rasa_sdk.executor import CollectingDispatcher
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import openai
import gspread
import random

class ActionParseUserText(Action):
    
    def name(self) -> Text:
        return "action_parse_user_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        openai.api_key = "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"
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        # df = pd.DataFrame({'user_text': [user_text], 'intent': [intent]})
        
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Return an answer for the text + {intent} combination: " + user_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        dispatcher.utter_message('mes_inte: ' + str(intent))

        return []


class ActionCannabisInfo(Action):
    def name(self) -> Text:
        return "action_cannabis_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Technical support: " + user_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        if intent == "ask_cannabis_info":
            dispatcher.utter_message("Cannabis is a plant that is used for medicinal and recreational purposes. The most commonly used part of the plant is the flowers or buds, which contain the psychoactive compounds delta-9-tetrahydrocannabinol (THC) and cannabidiol (CBD). THC is responsible for the “high” associated with cannabis use.")
        else:
            dispatcher.utter_message("I'm sorry, I do not have information on that.")

        return []
    
    # def get_answers_from_sheets(self, intent):
    #     # Connect to Google Sheets
    #     scope = ['https://spreadsheets.google.com/feeds',
    #             'https://www.googleapis.com/auth/drive']
    #     credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
    #     gc = gspread.authorize(credentials)

    #     # Open the sheet
    #     sh = gc.open("Answers Sheet")

    #     # Get the worksheet by name
    #     worksheet = sh.worksheet("Answers")

    #     # Get all the values from the worksheet
    #     data = worksheet.get_all_values()

    #     # Create a dataframe from the values
    #     df = pd.DataFrame(data[1:], columns=data[0])

    #     # Filter the dataframe by the intent
    #     answers = df[df['Intent'] == intent]['Answer'].tolist()

    #     return answers


class ActionTechSupport(Action):
    def name(self) -> Text:
        return "action_tech_support"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        openai.api_key = "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"
        user_text = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent').get('name')
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Technical support: " + user_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        
        if intent == "ask_tech_support":
            dispatcher.utter_message(text="Our technical support team is available 24/7 to assist you with any issues you may be having.")  #. Please send an email to support@cannabischatbot.com with a detailed description of your problem and we will get back to you as soon as possible.")
        else:
            dispatcher.utter_message(text="I'm sorry, I do not have information on that.")

        return []