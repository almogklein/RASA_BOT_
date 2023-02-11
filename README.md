# Rasa Bootstrap Chatbot #

A bootstrapped chatbot built using the open-source conversational AI platform, Rasa. This chatbot has access to both Google Sheets and the OpenAI ChatGPT API, making it a powerful tool for generating answers to a wide range of questions.

# Features
- Built using Rasa conversational AI platform
- Access to Google Sheets
- Access to OpenAI ChatGPT API

# Requirements
- Rasa
- Google API Client Library for Python
- OpenAI API Key

# Hardware Requirements
- 2 GHz dual-core processor or better
- 4 GB of RAM or more
- 20 GB of free hard disk space or more

# Setup
```
conda create --name myenv
conda activate myenv

pip install -U rasa
pip install google-api-python-client
pip install openai

git clone https://github.com/<username>/rasa-bootstrap-chatbot.git
cd rasa-bootstrap-chatbot
```
Replace <SHEET_URL> and API_KEY in the code with your Google Sheets URL and OpenAI API key respectively.

```
rasa train
rasa shell<OR>run
```

# Usage
The chatbot can be used to generate answers to a wide range of questions by accessing data stored in Google Sheets or using the OpenAI ChatGPT API. The user can specify the source of the answer (Google Sheets or ChatGPT) and the chatbot will return the appropriate response.
