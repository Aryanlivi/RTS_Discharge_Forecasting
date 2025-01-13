from dotenv import load_dotenv
import os 
import sys
from datetime import datetime
# Add the parent directory of src to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Service.Database import Database
load_dotenv()

date=datetime.fromisoformat('2025-01-13 13:44:23')
data_to_insert = {
    'datetime': date.strftime('%Y-%m-%d %H:%M'),
    'discharge': 100.5  # Example discharge value
}
SIURENITAR_TABLE=os.getenv('siurenitar_table')
db=Database()
db.connect()
query=f'''
SELECT * FROM {SIURENITAR_TABLE}
'''
db.insert_data(SIURENITAR_TABLE,data_to_insert)
db.disconnect()
