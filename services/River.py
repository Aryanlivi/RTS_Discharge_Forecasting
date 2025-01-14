import math 
from datetime import datetime,timedelta
from RiverForecast import RiverForecast
class River:
    #Predefined const for different Rivers:
    RIVER_CONSTANTS={
        'Galchi':{'distance':30000,'a':174.033420951409,'b':1.23635884471447,'c':365.6,'vel_a':1.725,'vel_b':628.5},
        'Budhi':{'distance':18500,'a':417.1536,'b':0.36303508,'c':333.40,'vel_a':6.533,'vel_b':2176},
    }
    def __init__(self,river_name,date_time,water_level):
        self.river_name=river_name
        self.date_time=datetime.fromisoformat(date_time)  # Convert to datetime object
        self.water_level=water_level
        self.discharge=None
        self.mean_velocity=None
        self.time_delay=None
        self.forecasted_data=None
        
        # Get predefined constants for the river
        if river_name in River.RIVER_CONSTANTS:
            self.constants = River.RIVER_CONSTANTS[river_name]
        else:
            raise ValueError(f"River name '{river_name}' not found in predefined constants.")

    def get_river_name(self):
        return self.river_name
    
    def get_river_constants(self):
        return self.constants
    
    def get_data(self):
        return {'datetime':self.date_time.isoformat(),'water_level':self.water_level}
    def set_discharge(self):
        
        a = self.constants['a']
        b = self.constants['b']
        c = self.constants['c']
        
        difference = self.water_level - c
        power=difference**b
        discharge=a*power
        self.discharge=float(discharge)
    
    def get_discharge(self):
        return self.discharge

    def set_mean_velocity(self):
        vel_a = self.constants['vel_a']
        vel_b=self.constants['vel_b']
        self.mean_velocity= vel_a*self.water_level-vel_b
        
    def get_mean_velocity(self):
        return self.mean_velocity
    
    def set_time_delay(self):
        
        distance=self.constants['distance']
        if math.isnan(self.mean_velocity) or self.mean_velocity == 0:
            self.time_delay= float('nan')
        
        self.time_delay = distance / (self.mean_velocity) # in seconds
    def get_time_delay(self):
        return self.time_delay
    
        
        
    def round_down_to_nearest_ten(self,forecasted_datetime):
        """
        Rounds the given time **down** to the nearest 10 minutes (i.e., 00, 10, 20, 30, 40, 50).
        """
        # Get the number of minutes
        minutes = forecasted_datetime.minute
        
        # Round down to the nearest 10 minutes
        rounded_minutes = (minutes // 10) * 10  # Simply discard the remainder
        
        # Handle case where rounding to the nearest 10 doesn't overflow
        forecasted_datetime = forecasted_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
        return forecasted_datetime


    def compute_and_get_forecast(self):
        self.set_discharge()
        self.set_mean_velocity()
        self.set_time_delay()
        
        if self.time_delay:  
            forecasted_datetime = self.date_time + timedelta(seconds=self.time_delay)
            forecasted_datetime=self.round_down_to_nearest_ten(forecasted_datetime)
            self.forecasted_data=RiverForecast(self.river_name,forecasted_datetime,self.discharge)
            return self.forecasted_data
    
        
    def get_forecasted_data(self):
        return self.forecasted_data