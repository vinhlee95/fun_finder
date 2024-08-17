import psycopg2

conn = psycopg2.connect(
  dbname="tennis_reservation",
  user="vinhle",
  host="localhost",
  port="5432",
)

cur = conn.cursor()

# Test
cur.execute("select * from available_reservation where date = '2024-08-18' and court_id = 'Court 2'")

records = cur.fetchall()

for record in records:
  print(record)