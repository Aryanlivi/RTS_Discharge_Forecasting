from River import River
from dotenv import load_dotenv
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Socket.ApiService import APIService
# from DB_Service.Database import Database
from datetime import datetime,timedelta
from RiverForecast import RiverForecast
from services.db_sessions import Database
from models.forecast_models import ForecastBudhiToSiurenitar,ForecastGalchiToSiurenitar,ForecastSiurenitarData


load_dotenv()

class ForecastManager:
    #ENV CONSTANTS
    SIURENITAR_TABLE=os.getenv('siurenitar_table')
    SocketGalchiId=os.getenv('SocketGalchiId')
    SocketBudhiId=os.getenv('SocketBudhiId')

    def __init__(self, data):
        self.data = data
        self.db = Database()
        # self.changed_rows=[]
        
    def get_river_data(self,data, id):
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

    

    def compute_combined_forecast(self,galchi_forecast:RiverForecast,budhi_forecast:RiverForecast):
        latest_forecast_datetime= max(galchi_forecast.date_time, budhi_forecast.date_time)
        try:
            if latest_forecast_datetime is None:
                return
            galchi_river_value=None  
            budhi_river_value=None
            if latest_forecast_datetime==galchi_forecast.date_time:
                galchi_river_value=galchi_forecast.discharge
                budhi_river_value=self.db.fetch_latest_discharge(ForecastBudhiToSiurenitar,latest_forecast_datetime)
            elif latest_forecast_datetime==budhi_forecast.date_time:
                galchi_river_value=self.db.fetch_latest_discharge(ForecastGalchiToSiurenitar,latest_forecast_datetime)
                budhi_river_value=budhi_forecast.discharge
            else:
                print("ERROR :Latest Date time doesnt match!")
                return
            total_discharge=0
            
            if galchi_river_value is not None and budhi_river_value is not None:
                total_discharge = galchi_river_value + budhi_river_value
            
            data = {
                'datetime': latest_forecast_datetime,
                'discharge': total_discharge
            }

            self.db.insert_or_update(ForecastSiurenitarData,data)
            # new_data=self.db.get_row_by_datetime(ForecastSiurenitarData,latest_forecast_datetime)
            # self.changed_rows.append(new_data)
            print("---------------appended the created row to changed_rows-------------")
            return True, latest_forecast_datetime
        except Exception as e:
            print(f"Error updating Suirenitar table: {e}")
            
    def revisit_and_update_combined_river_forecast(self,galchi_forecast:RiverForecast,budhi_forecast:RiverForecast):
        all_rows=[]
        try:
            # Fetch all rows in siurenitar_table
            
            combined_river_rows = self.db.session.query(ForecastSiurenitarData).all()
            for combined_river in combined_river_rows:
                combined_river_datetime = combined_river.datetime                
                galchi_discharge = self.db.fetch_latest_discharge(ForecastGalchiToSiurenitar,combined_river_datetime)
                budhi_discharge = self.db.fetch_latest_discharge(ForecastBudhiToSiurenitar,combined_river_datetime)
                # Calculate the total discharge
                total_discharge = galchi_discharge + budhi_discharge
                self.db.update_discharge(ForecastSiurenitarData,combined_river_datetime,total_discharge)
                # Fetch and return all rows after updating
            all_rows =self.db.fetch_all_rows(ForecastSiurenitarData)
            print(all_rows)
            print("==============")
            return all_rows
            #     updated_row = self.db.get_row_by_datetime(ForecastSiurenitarData, combined_river_datetime)
            #     if updated_row:
            #         self.changed_rows.append(updated_row)  # Add updated row to the list of changed rows
            # return self.changed_rows
        except Exception as e:
            print(f"Error recalculating: {e}")
        return None

    def compute(self):
        galchi_data=self.get_river_data(data=self.data,id=ForecastManager.SocketGalchiId)
        budhi_data=self.get_river_data(data=self.data,id=ForecastManager.SocketBudhiId) 
        # Retrieve data for Galchi and Budhi rivers (for tests here)
        # galchi_data = {'datetime': '2025-01-13T15:10:00+00:00', 'value': 366.051483154}
        # budhi_data = {'datetime': '2025-01-13T15:20:00+00:00', 'value': 333.470916748}

        if not galchi_data or not budhi_data:
            return [{'time':datetime.now(),'value':-999999}]

        # Create river forecast objects
        galchi=River('Galchi',galchi_data['datetime'],galchi_data['value'])
        budhi=River('Budhi',budhi_data['datetime'],budhi_data['value'])

        # Compute forecasts
        galchi_forecast = galchi.compute_and_get_forecast()
        budhi_forecast = budhi.compute_and_get_forecast()


        # print(f"Original Galchi:{galchi.get_data()}")
        # print(f"Original Budhi:{galchi.get_data()}")
        # print('-------------------------------------------')
        # # Output the forecasts
        # print(f"Galchi Forecasted: {galchi_forecast.get_data()}")
        # print(f"Budhi Forecasted: {budhi_forecast.get_data()}")

        #test forecasted:
        
        # test1=RiverForecast('Galchi',datetime.fromisoformat('2025-01-13 18:10'),40)
        # test2=RiverForecast('Budhi',datetime.fromisoformat('2025-01-13 17:30'),10)
        
        self.db.insert_or_update(ForecastGalchiToSiurenitar, galchi_forecast.get_data())
        self.db.insert_or_update(ForecastBudhiToSiurenitar, budhi_forecast.get_data())
        
        self.compute_combined_forecast(galchi_forecast,budhi_forecast)
        all_rows=self.revisit_and_update_combined_river_forecast(galchi_forecast,budhi_forecast)
        return all_rows

    
    
    def convert_to_nepali_datetime(self,utc_datetime):
        # # Parse the UTC datetime string to a datetime object
        # utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%d %H:%M:%S")
        
        # Define the NST offset (5 hours and 45 minutes)
        nst_offset = timedelta(hours=5, minutes=45)
        
        # Add the offset to convert to NST
        nepali_datetime = utc_datetime + nst_offset
        
        # Format and return the Nepali datetime
        return nepali_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def post(self):
        data=self.compute()
        
        # print(f"original data{data}")
        for ele in data: 
            ele['time']=self.convert_to_nepali_datetime(ele['time'])
        print("------------")
        print(data)
        api_service=APIService()
        api_service.post_forecast(data)
    
    
