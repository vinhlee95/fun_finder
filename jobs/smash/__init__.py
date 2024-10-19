import requests
from datetime import datetime, timedelta
import pprint
import pytz

from dotenv import load_dotenv
load_dotenv()


logger = pprint.PrettyPrinter(indent=2)

# Example: https://api.smash.fi/api/1.0/reservations/?productid=15&date=2023-04-04
SMASH_ESPOO_URL = "https://api.smash.fi/api/1.0/reservations/?productid=15"

def get_smash_reservations(date_object: datetime):
  """Get the number of reservations for a given date."""
  date = date_object.strftime("%Y-%m-%d")
  url = f"{SMASH_ESPOO_URL}&date={date}"
  response = requests.get(url)
  response.raise_for_status()
  return response.json()

def get_hour_number(time: str) -> int:
  date_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
  minute = date_object.minute

  # If the minute is greater than 30, round the hour up
  if minute >= 30:
    return int(date_object.hour) + 1

  return int(date_object.hour)

def get_reservations_with_time(reservations):
  """Get start and end of reservations."""
  results = []

  for reservation in reservations:
    start = get_hour_number(reservation.get("start"))
    end = get_hour_number(reservation.get("end"))

    # end-start = 0 when a reservation is only for 30 minutes
    # skip looking for a 30-minute availability
    if end - start <= 1:
      results.append({
        "start": start,
        "end": end,
        "reserved_hours": [start]
      })
    else:
      results.append({
        "start": start,
        "end": end,
        "reserved_hours": [hour for hour in range(start, end)]
      })
  
  return results

def get_unique_court_id(reservations):
  """Get a list of unique court ids."""
  return list(set([reservation.get("resources", [])[0].get("resourceId") for reservation in reservations]))

def map_court_id_to_name(court_id: int):
  # Map court id to name so that it is easier to read the data
  court_id_to_name = {
    44: "Court 1",
    45: "Court 2",
    46: "Court 3",
  }
  return court_id_to_name.get(court_id)


def fetch_available_start_hour_by_date(date_obj: datetime = datetime.now()):
  response = get_smash_reservations(date_obj)
  reservations = response.get("rows")
  # logger.pprint(reservations[:5])
  court_ids = get_unique_court_id(reservations)

  # Sort reservation by courts, format the data to have only start and end time
  reservations_by_court = {}
  for court_id in court_ids:
    reservations_by_court[court_id] = get_reservations_with_time([reservation for reservation in reservations if reservation.get("resources", [])[0].get("resourceId") == court_id])

  # Get available start hour for each court
  available_slots_by_court = {}
  for court_id, reservations in reservations_by_court.items():
    # Get a list of unique start hours from reserved_hours
    reserved_start_hours = list(set([hour for reservation in reservations for hour in reservation.get("reserved_hours")]))

    # print("Reserved starting hours", reserved_start_hours)

    # TODO: different start and end hours for weekdays and weekends
    POSSIBLE_STARTING_HOUR = 7
    LATEST_AVAILABLE_HOUR = 23
    available_start_hour = [hour for hour in range(POSSIBLE_STARTING_HOUR, LATEST_AVAILABLE_HOUR) if hour not in reserved_start_hours]

    court_name = map_court_id_to_name(court_id)
    available_slots_by_court[court_name] = available_start_hour
    
  # Convert to UTC
  utc_date_obj = date_obj.astimezone(pytz.utc)
  
  # Format datetime object to YYY-MM-DD
  formatted_date = utc_date_obj.strftime("%Y-%m-%d")

  return {
    formatted_date: available_slots_by_court
  }


def fetch_smash_olari_availability(for_next_n_days: int = 8):
  print(f"Fetching Smash Olari availability for the next {for_next_n_days} days")
  # Fetch reservations for the next month
  available_slots = []

  for i in range(0, for_next_n_days):
    available_reservation_for_date = fetch_available_start_hour_by_date((datetime.now() + timedelta(days=i)))
    available_slots.append(available_reservation_for_date)

  return available_slots


# Enable following lines to save the response to a file with command: python smash_olari.py > example_response/smash.json
# available_slots = fetch_smash_olari_availability(2)
# print(available_slots)