import logging
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import sys
# Add the parent directory of src to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# Configure logging at the start of your script (if not already configured)
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("services/Socket/logs/api_log.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)
class APIService:
    def __init__(self):
        self.base_url = os.getenv('baseURL')
        self.origin_code = os.getenv('origin_code')
        self.parameter_code = os.getenv('parameter_code')
        self.token = os.getenv('token')
        
    def post_forecast(self,data):
        url = f'{self.base_url}/import'
        for item in data:
            item['origin_code']=self.origin_code
            item['parameter_code']=self.parameter_code
            
        headers = {
        'Content-Type': 'application/json',
        'Authorization': self.token
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                logging.info("Post operation completed successfully.")
                logging.info(f"Posted data: {data}")
                logging.info(f"API response: {response.json()}")
                return response.json(), response.status_code, None
            else:
                return None, response.status_code, response.text
        except Exception as e:
            return None, None, str(e)
