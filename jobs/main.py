from smash import fetch_smash_olari_availability


def main():
  # Fetch available slots from Smash API
  available_slots = fetch_smash_olari_availability(2)

  print(available_slots)
  return

main()