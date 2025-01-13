from River import River
from dotenv import load_dotenv
from Utils import get_river_data
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Socket.ApiService import APIService
from DB_Service.Database import Database
from datetime import datetime
from RiverForecast import RiverForecast



load_dotenv()

class ForecastManager:
    #ENV CONSTANTS
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
        return max(forecast1.date_time, forecast2.date_time)
    
    def get_latest_discharge_from_db(self, table_name, datetime):
        try:
            query = f"""
                SELECT dateTime, discharge FROM {table_name}
                WHERE dateTime <= '{datetime}'
                ORDER BY dateTime DESC
                LIMIT 1;
            """
            result = self.db.fetch(query)
            if result:
                return result[0][1]  # Returns the discharge value of the latest row
        except Exception as e:
            print(f"Error fetching rows up to {datetime} from {table_name}: {e}")
        return None 

    def compute_and_update_combined_river_forecast(self,forecast1:RiverForecast,forecast2:RiverForecast):
        latest_forecast_datetime=self.get_latest_datetime(forecast1,forecast2)
        try:
            if latest_forecast_datetime is None:
                return
            river1_value=None
            river2_value=None
            if latest_forecast_datetime==forecast1.date_time:
                river1_value=forecast1.discharge
                river2_value=self.get_latest_discharge_from_db(forecast2.get_db_table_name(),latest_forecast_datetime)
            elif latest_forecast_datetime==forecast2.date_time:
                river1_value=self.get_latest_discharge_from_db(forecast1.get_db_table_name(),latest_forecast_datetime)
                river2_value=forecast2.discharge
            else:
                print("ERROR :Latest Date time doesnt match!")
                return
            total_discharge=0
            
            if river1_value is not None and river2_value is not None:
                total_discharge = river1_value + river2_value
            update_query = f"""
                INSERT INTO {ForecastManager.SIURENITAR_TABLE} (dateTime, discharge) 
                VALUES ('{latest_forecast_datetime}', {total_discharge})
                ON CONFLICT (dateTime)
                DO UPDATE SET discharge = EXCLUDED.discharge
                """
            self.db.execute_query(update_query)
            return True, latest_forecast_datetime
        except Exception as e:
            print(f"Error updating Suirenitar table: {e}")
            
    def revisit_and_update_combined_river_forecast(self,forecast1:RiverForecast,forecast2:RiverForecast):
        try:
            # Fetch all rows in siurenitar_table
            query_combined_river= f"SELECT dateTime FROM {ForecastManager.SIURENITAR_TABLE}"
            combined_river_rows = self.db.fetch(query_combined_river)

            
            for combined_river in combined_river_rows:
                combined_river_datetime = combined_river[0]

                
                river1_discharge = self.get_latest_discharge_from_db(forecast1.get_db_table_name(),combined_river_datetime)
                river2_discharge = self.get_latest_discharge_from_db(forecast2.get_db_table_name(),combined_river_datetime)
                # Calculate the total discharge
                total_discharge = river1_discharge + river2_discharge
                # Update the siurenitar_table for this dateTime  
                update_query = f"""
                    UPDATE {ForecastManager.SIURENITAR_TABLE}
                    SET discharge = {total_discharge}
                    WHERE dateTime = '{combined_river_datetime}'
                """
                self.db.execute_query(update_query)
        except Exception as e:
            print(f"Error recalculating {ForecastManager.SIURENITAR_TABLE}: {e}")
        return None

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
        galchi_forecast = galchi.compute_and_get_forecast()
        budhi_forecast = budhi.compute_and_get_forecast()

        # Output the forecasts
        print(f"Galchi Forecasted: {galchi_forecast}")
        print(f"Budhi Forecasted: {budhi_forecast}")
        print('-------------------------------------------')

        
        #test forecasted:
        test1=RiverForecast('Galchi','2025-01-13 21:25',110)
        test2=RiverForecast('Budhi','2025-01-13 22:25',290)
        # Connect to the database and insert data
        self.db.connect()
        self.db.insert_data(galchi_forecast.get_db_table_name(), test1.get_data())
        self.db.insert_data(budhi_forecast.get_db_table_name(), test2.get_data())
        
        self.compute_and_update_combined_river_forecast(test1,test2)
        self.revisit_and_update_combined_river_forecast(test1,test2)
        self.db.disconnect()

# Run the forecast computation and posting
forecast_manager = ForecastManager({})
forecast_manager.compute_and_post()
