from River import River
from dotenv import load_dotenv
from Utils import get_river_data
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Socket.ApiService import APIService
from DB_Service.Database import Database
from datetime import datetime



load_dotenv()

class ForecastManager:
    #ENV CONSTANTS:
    GALCHI_TABLE=os.getenv('galchi_table')
    BUDHI_TABLE=os.getenv('budhi_table')
    SIURENITAR_TABLE=os.getenv('siurenitar_table')

    SocketGalchiId=os.getenv('SocketGalchiId')
    SocketBudhiId=os.getenv('SocketBudhiId')

    def __init__(self, data):
        self.data = data
        self.db = Database()
        
    def get_river_data(data, id):
        try:
            if isinstance(data, list):
                if not data:  # Check if the list is empty
                    return None 
                for item in data:
                    if item.get('id') == int(id):
                        return item.get('waterLevel', 'Water level not available')
                return None 
            else:
                return 'Invalid data format received.'  

        except Exception as error:
            return f"Error: {error}"  

    def get_latest_datetime(self, forecast1, forecast2):
        # Find the latest datetime between two forecasts
        if forecast1['datetime'] > forecast2['datetime']:
            return forecast1['datetime']
        else:
            return forecast2['datetime']

    def compute_and_post(self):
        
        # galchi_data=self.get_river_data(data=self.data,id=ForecastManager.SocketGalchiId)
        # budhi_data=self.get_river_data(data=self.data,id=ForecastManager.SocketBudhiId)
        
        # Retrieve data for Galchi and Budhi rivers (for tests here)
        galchi_data = {'datetime': '2025-01-13T08:55:00+00:00', 'value': 366.051483154}
        budhi_data = {'datetime': '2025-01-13T08:55:00+00:00', 'value': 333.470916748}

        if not galchi_data or not budhi_data:
            return

        # Create river forecast objects
        galchi=River('Galchi',galchi_data['datetime'],galchi_data['value'])
        budhi=River('Budhi',budhi_data['datetime'],budhi_data['value'])

        # Compute forecasts
        galchi_forecasted = galchi.compute_and_get_forecast()
        budhi_forecasted = budhi.compute_and_get_forecast()

        # Output the forecasts
        print(f"Galchi Forecasted: {galchi_forecasted}")
        print(f"Budhi Forecasted: {budhi_forecasted}")
        print('-------------------------------------------')

        # Get latest forecast datetime
        latest_forecast_datetime = self.get_latest_datetime(galchi_forecasted, budhi_forecasted)
        print(f"Latest Forecast Datetime: {latest_forecast_datetime}")

        # Connect to the database and insert data
        self.db.connect()
        self.db.insert_data(ForecastManager.GALCHI_TABLE, galchi_forecasted)
        self.db.insert_data(ForecastManager.BUDHI_TABLE, budhi_forecasted)
        self.db.disconnect()

# Run the forecast computation and posting
forecast_manager = ForecastManager({})
forecast_manager.compute_and_post()
