from datetime import datetime,timedelta



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
    # Fix edge case where new_minutes becomes negative
    if new_minutes < 0:
        new_minutes += 60
        hours = (forecasted_datetime.hour - 1) % 24  # Decrement hour and wrap around at 0
    else:
        hours = forecasted_datetime.hour
    if new_minutes >= 60:
        new_minutes -= 60
        hours = (hours + 1) % 24  # Increment hour and wrap around at 24

    # Adjust the datetime to the rounded minutes
    forecasted_datetime = forecasted_datetime.replace(hour=hours, minute=new_minutes, second=0, microsecond=0)
    return forecasted_datetime


def round_down_to_nearest_ten(forecasted_datetime):
        """
        Rounds the given time **down** to the nearest 10 minutes (i.e., 00, 10, 20, 30, 40, 50).
        """
        print(forecasted_datetime)
        # Get the number of minutes
        minutes = forecasted_datetime.minute
        
        # Round down to the nearest 10 minutes
        rounded_minutes = (minutes // 10) * 10  # Simply discard the remainder
        
        # Handle case where rounding to the nearest 10 doesn't overflow
        forecasted_datetime = forecasted_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
        return forecasted_datetime
    
date_time='2025-01-13T10:00:00+00:00'
date_time=datetime.fromisoformat(date_time)

# 18:10
time_delay=8884
forecasted_datetime=date_time+timedelta(seconds=time_delay)
print(round_down_to_nearest_ten(forecasted_datetime))
  
    
# def round_to_nearest_five(forecasted_datetime):
#     """
#     Rounds the given time to the nearest 05, 15, 25, etc. with 10-minute gaps.
#     """
#     print(forecasted_datetime)
#     # Calculate the remainder when minutes is divided by 10
#     remainder = forecasted_datetime.minute % 10
#     # Determine the new minutes based on the remainder
#     if remainder < 5:
#         new_minutes = (forecasted_datetime.minute // 10) * 10 - 5
#     elif remainder == 5:
#         new_minutes = forecasted_datetime.minute
#     else:
#         new_minutes = (forecasted_datetime.minute // 10 + 1) * 10 - 5


#     # Handle case where rounding increases minutes past 59
#     hours = forecasted_datetime.hour
#     if new_minutes >= 60:
#         new_minutes = 0
#         hours = (hours + 1) % 24  # Increment hour and wrap around at 24

#     # Adjust the datetime to the rounded minutes
#     forecasted_datetime = forecasted_datetime.replace(hour=hours, minute=new_minutes, second=0, microsecond=0)
#     return forecasted_datetime

# def round_to_nearest_ten(forecasted_datetime):
#     """
#     Rounds the given time to the nearest 10 minutes (i.e., 00, 10, 20, 30, 40, 50).
#     """
#     print(forecasted_datetime)
#     # Get the number of minutes
#     minutes = forecasted_datetime.minute
    
#     # Round to nearest 10 minutes
#     rounded_minutes = (minutes // 10) * 10
#     if minutes % 10 >= 5:
#         rounded_minutes += 10

#     # Handle case where rounding increases minutes past 59 (e.g., 55 -> 00 and increment hour)
#     if rounded_minutes == 60:
#         rounded_minutes = 0
#         forecasted_datetime = forecasted_datetime + timedelta(hours=1)
    
#     # Replace the datetime with the rounded minutes
#     forecasted_datetime = forecasted_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
#     return forecasted_datetime

# def round_down_to_nearest_ten(forecasted_datetime):
#     """
#     Rounds the given time **down** to the nearest 10 minutes (i.e., 00, 10, 20, 30, 40, 50).
#     """
#     print(forecasted_datetime)
#     # Get the number of minutes
#     minutes = forecasted_datetime.minute
    
#     # Round down to the nearest 10 minutes
#     rounded_minutes = (minutes // 10) * 10  # Simply discard the remainder
    
#     # Handle case where rounding to the nearest 10 doesn't overflow
#     forecasted_datetime = forecasted_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
#     return forecasted_datetime


