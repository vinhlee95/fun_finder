import psycopg2
from langchain.tools import tool
from pydantic.v1 import BaseModel


conn = psycopg2.connect(
  dbname="tennis_reservation",
  user="vinhle",
  host="localhost",
  port="5432",
)

def list_tables():
  cur = conn.cursor()
  cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
  tables = cur.fetchall()
  return tables

class RunQueryToolArgSchema(BaseModel):
  query: str

@tool(
  args_schema=RunQueryToolArgSchema
)
def run_query_tool(query):
  """
  Given a query string, run the query and return the result.
  """
  try:
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()
  except Exception as e:
    return f"An exception occurred {str(e)}"
  

class DescribeTableSchema(BaseModel):
  tables: list[str]

@tool(
  args_schema=DescribeTableSchema,
)
def describe_tables_tool(tables: list[str]):
  """
  Given a list of table names, return SQL schema of these tables
  """
  cur = conn.cursor()
  result = []
  for table in tables:
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}';")
    result.append(cur.fetchall())
  return result
