from db.available_slot import AvailableSlotSchema, persist_available_slot
from smash import fetch_smash_olari_availability

def save_available_slots(available_slots: dict):
  for date, slots in available_slots.items():
    for court_id, hours in slots.items():
      print(date, court_id, hours)
      for hour in hours:
        available_slot = AvailableSlotSchema(date=date, court_id=court_id, available_hour=hour)
        persist_available_slot(available_slot)


def main():
  # Fetch available slots from Smash API
  save_available_slots(fetch_smash_olari_availability(2)[0])
  return

main()