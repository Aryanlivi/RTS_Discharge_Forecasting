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

    # Handle case where rounding increases minutes past 59
    hours = forecasted_datetime.hour
    if new_minutes >= 60:
        new_minutes -= 60
        hours = (hours + 1) % 24  # Increment hour and wrap around at 24

    # Adjust the datetime to the rounded minutes
    forecasted_datetime = forecasted_datetime.replace(hour=hours, minute=new_minutes, second=0, microsecond=0)
    return forecasted_datetime



date_time='2025-01-13T16:28:00+00:00'
date_time=datetime.fromisoformat(date_time)

# 18:10
time_delay=6988.933319445655
forecasted_datetime=date_time+timedelta(seconds=time_delay)
print(round_to_nearest_five(forecasted_datetime))

