from google.generativeai import list_models
from dotenv import load_dotenv
import pprint
import os

load_dotenv(dotenv_path='.env')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

models = list_models()
for model in models:
    pprint.print(model.name)