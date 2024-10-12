from db.available_slot import AvailableSlotSchema, persist_available_slot
from tennismesta import fetch_tennismesta_availability
from smash import fetch_smash_olari_availability

DEFAULT_PERIOD = 7

# {
#   "date": {
#     "court_id": [hour1, hour2, ...]
#   }
# }
type DailyAvailableSlot = dict[str, dict[str, list[int]]]

def save_available_slots_for_day(available_slots: DailyAvailableSlot, court_name: str):
  for date, slots in available_slots.items():
    for court_id, hours in slots.items():
      for hour in hours:
        available_slot = AvailableSlotSchema(date=date, court_id=court_id, available_hour=hour, court_name=court_name)
        persist_available_slot(available_slot)

def save_available_slots_for_period(available_slots: list[DailyAvailableSlot], court_name: str):
  for daily_slots in available_slots:
    save_available_slots_for_day(daily_slots, court_name)


def main():
  try:
      # Fetch available slots from Smash API
    print("🔍 fetching available slots for Smash Olari")
    save_available_slots_for_period(fetch_smash_olari_availability(DEFAULT_PERIOD), "Smash Olari")
    print("✅ successfully saved available slots for Smash Olari")

    print("🔍 fetching available slots for Tennismesta")
    save_available_slots_for_period(fetch_tennismesta_availability(DEFAULT_PERIOD), "Tennismesta")
    print("✅ successfully saved available slots for Tennismesta")

    print("✅ successfully saved available slots of ALL COURTS to DB")
    return
  except Exception as e:
    print(f"❌ failed to save available slots to DB {str(e)}")
    return


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"❌ failed to save available slots to DB {str(e)}")
    exit(1)