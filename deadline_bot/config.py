import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GOOGLE_API_CREDENTIAL = os.path.dirname(os.path.abspath(__file__)) + '/google_api_credential.json'
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
