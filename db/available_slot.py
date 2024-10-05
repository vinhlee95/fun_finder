from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from db.db import conn
from pydantic.v1 import BaseModel

class AvailableSlotSchema(BaseModel):
  date: str
  court_id: str
  available_hour: int
  court_name: str

def persist_available_slot(available_slot: AvailableSlotSchema) -> None:
  cur = conn.cursor()
  cur.execute(
    """
    INSERT INTO available_slots (date, court_id, available_hour, court_name) VALUES (%s, %s, %s, %s) 
    ON CONFLICT (date, court_id, available_hour) DO NOTHING
    """,
    (available_slot.date, available_slot.court_id, available_slot.available_hour, available_slot.court_name)
  )
  conn.commit()
  return


Base = declarative_base()

class AvailableSlot(Base):
    __tablename__ = 'available_slots'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    court_id = Column(String, nullable=False)
    available_hour = Column(Integer, nullable=False)
    court_name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('date', 'court_id', 'available_hour', name='unique_slot'),
    )
