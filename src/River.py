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
        # print(f"time_delay:{self.time_delay}")
    def get_time_delay(self):
        return self.time_delay
    
    
    def round_to_nearest_five(forecasted_datetime):
        """
        Rounds the given time to the nearest 05, 15, 25, etc. with 10-minute gaps.
        """
        print(forecasted_datetime)
        # Calculate the remainder when minutes is divided by 10
        remainder = forecasted_datetime.minute % 10
        # Determine the new minutes based on the remainder
        if remainder < 5:
            new_minutes = (forecasted_datetime.minute // 10) * 10 - 5
        elif remainder == 5:
            new_minutes = forecasted_datetime.minute
        else:
            new_minutes = (forecasted_datetime.minute // 10 + 1) * 10 - 5

        # Handle case where rounding increases minutes past 59
        hours = forecasted_datetime.hour
        if new_minutes >= 60:
            new_minutes -= 60
            hours = (hours + 1) % 24  # Increment hour and wrap around at 24

        # Adjust the datetime to the rounded minutes
        forecasted_datetime = forecasted_datetime.replace(hour=hours, minute=new_minutes, second=0, microsecond=0)
        return forecasted_datetime


    def compute_and_get_forecast(self):
        self.set_discharge()
        self.set_mean_velocity()
        self.set_time_delay()
        
        if self.time_delay:  
            print(self.time_delay)
            forecasted_datetime = self.date_time + timedelta(seconds=self.time_delay)
            forecasted_datetime=self.round_to_nearest_five(forecasted_datetime)
            self.forecasted_data=RiverForecast(self.river_name,forecasted_datetime,self.discharge)
            return self.forecasted_data
    
        
    def get_forecasted_data(self):
        return self.forecasted_data