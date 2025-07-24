from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

api_key = os.environ.get('GOOGLE_API_KEY')
print(api_key)
