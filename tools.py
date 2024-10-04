from langchain.tools import tool
from datetime import datetime, timedelta
import pytz

@tool()
def get_next_weekday(phrase: str):
    """
    Return the date for the specified weekday phrase (e.g., "this Friday", "next Tuesday")
    in the format "YYYY-MM-DD" in EET timezone.
    """
    eet = pytz.timezone('Europe/Helsinki')
    today = datetime.now(eet)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    parts = phrase.split()
    if len(parts) == 2 and (parts[0] not in ["this", "next"] or parts[1] not in weekdays):
        raise ValueError("Invalid phrase. Please use format 'this <weekday>' or 'next <weekday>'.")
    
    if len(parts) == 1 and parts[0] != "today":
        raise ValueError("Invalid phrase. Please use format 'this <weekday>' or 'next <weekday>'.")

    if parts[0] == "today":
        return today.strftime('%Y-%m-%d')
    
    target_weekday = parts[1]
    target_weekday_index = weekdays.index(target_weekday)
    days_ahead = target_weekday_index - today.weekday()

    if parts[0] == "this":
        if days_ahead < 0:  # Target day already happened this week
            days_ahead += 7
    elif parts[0] == "next":
        if days_ahead <= 0:  # Target day already happened this week or is today
            days_ahead += 7

    next_weekday = today + timedelta(days=days_ahead)
    return next_weekday.strftime('%Y-%m-%d')