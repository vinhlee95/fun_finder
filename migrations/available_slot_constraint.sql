ALTER TABLE available_slot
ADD CONSTRAINT unique_date_court_hour UNIQUE (date, court_id, available_hour);