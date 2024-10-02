from datetime import datetime, timedelta
import requests
import pprint
import pytz

logger = pprint.PrettyPrinter(indent=2)

# https://playtomic.io/api/v1/availability?user_id=me&tenant_id=e65484f9-9f82-45ea-8e14-fffde2b0fd64&sport_id=TENNIS&local_start_min=2023-03-28T00%3A00%3A00&local_start_max=2023-03-28T23%3A59%3A59
API_URL = "https://playtomic.io/api/v1/availability?user_id=me&sport_id=TENNIS"


def fetch_available_slots_for_date(sport_center_id: str, date: datetime):
    """
    Return type: 
    [
        {
            "resource_id": "court_1",
            "slots": [
                { "duration": 60, "price": "18.72 EUR", "start_time": "03:00:00" }
            ],
            "start_date": "2023-04-02"
        },
        {
            "resource_id": "court_2",
            "slots": [
                { "duration": 60, "price": "18.72 EUR", "start_time": "03:00:00" }
            ],
            "start_date": "2023-04-02"
        }
    ]
    """
    start_of_day = date.replace(hour=0, minute=0)
    end_of_day = date.replace(hour=23, minute=59)

    res = requests.get(f"{API_URL}", params={
        "tenant_id": sport_center_id,
        "local_start_min": start_of_day.isoformat(),
        "local_start_max": end_of_day.isoformat()
    })
    res.raise_for_status()
    return res.json()

def convert_to_full_date(date: datetime, hour_minute_second: str) -> datetime:
    hour_obj = datetime.strptime(hour_minute_second, "%H:%M:%S")
    return datetime.combine(date.date(), hour_obj.time())

def get_local_time_from_utc(date_obj: datetime) -> int:
    # Convert to UTC
    utc_tz = pytz.timezone("UTC")
    time_obj_utc = utc_tz.localize(date_obj)

    # Convert to Helsinki time
    helsinki_timezone = pytz.timezone("Europe/Helsinki")
    helsinki_local_time = time_obj_utc.astimezone(helsinki_timezone)

    # Return only the hour
    # return helsinki_local_time.strftime("%H:%M:%S")
    return helsinki_local_time.hour


def get_available_slot_with_info(current_date: datetime, slot: dict) -> int:
    local_start_time = get_local_time_from_utc(convert_to_full_date(current_date, str(slot.get("start_time"))))
    # Return only the hour for now
    return local_start_time
    # return {
    #     "start": local_start_time,
    #     "duration": slot.get("duration"),
    #     "price": slot.get("price")
    # }

def map_court_id_to_court_name(court_id: str) -> str:
    mapper = {
        "6cc1880b-57b0-440a-9196-d18ba68266e6": "Court 1",
        "d247e836-b93d-435c-9fb5-3298c2882b56": "Court 2"
    }
    return mapper.get(court_id, court_id)


def fetch_available_slots_by_sport_center_id(sport_center_id: str, for_next_n_days: int = 8) -> list[dict]:
    print(f"Fetching Playtomic court {sport_center_id} availability for the next {for_next_n_days} days")
    available_slots = []
    for i in range(0, for_next_n_days):
        date = datetime.now() + timedelta(days=i)
        res = fetch_available_slots_for_date(sport_center_id, date)
        formatted_date = date.isoformat()

        available_slots_for_date = {}
        
        for court_data in res:
            court_id = court_data.get("resource_id")
            slots = court_data.get("slots")
            available_hours = [get_available_slot_with_info(date, slot) for slot in slots]
            # Remove duplicated hours since we do not care about duration for now
            available_slots_for_date[map_court_id_to_court_name(court_id)] = list(set(available_hours))

        available_slots.append({
            formatted_date: available_slots_for_date
        })

    return available_slots


# Specific tenant ID for each sport center
SPORT_CENTER_ID = "e65484f9-9f82-45ea-8e14-fffde2b0fd64"

def fetch_tennismesta_availability(for_next_n_days: int = 7):
  available_slots = fetch_available_slots_by_sport_center_id(SPORT_CENTER_ID, for_next_n_days)
  return available_slots