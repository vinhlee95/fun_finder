from db.db import conn
from datetime import date
from pydantic.v1 import BaseModel

class AvailableSlotSchema(BaseModel):
  date: str
  court_id: str
  available_hour: int

def persist_available_slot(available_slot: AvailableSlotSchema) -> None:
  cur = conn.cursor()
  cur.execute(
    """
    INSERT INTO available_slot (date, court_id, available_hour) VALUES (%s, %s, %s) 
    ON CONFLICT (date, court_id, available_hour) DO NOTHING
    """,
    (available_slot.date, available_slot.court_id, available_slot.available_hour)
  )
  conn.commit()
  return
