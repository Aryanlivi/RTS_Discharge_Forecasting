from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()

class RiverForecast:
    CONSTANTS={
        'Galchi':{'Table':os.getenv('galchi_table')},
        'Budhi':{'Table':os.getenv('budhi_table')},
        'Siurenitar':{'Table':os.getenv('siurenitar_table')}
    }
    def __init__(self,river_name,date_time,discharge):
        self.river_name=river_name
        self.date_time=date_time
        self.discharge=discharge
        # Get predefined constants for the river
        if self.river_name in RiverForecast.CONSTANTS:
            self.constants = RiverForecast.CONSTANTS[self.river_name]
        else:
            raise ValueError(f"River name '{self.river_name}' not found in predefined constants.")

    def get_data(self):
        return {'datetime':self.date_time,
                'discharge':self.discharge}
    def get_db_table_name(self):
        return self.constants['Table']
        
