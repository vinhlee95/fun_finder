import os
import psycopg2
from langchain.tools import tool
from pydantic.v1 import BaseModel
from google.cloud.sql.connector import Connector

def get_db_connection():
  env = os.getenv("ENV")
  if env == "development":
    try:
      conn = psycopg2.connect(os.getenv("DATABASE_URL"))
      return conn
    except Exception as e:
      print(f"An exception occurred {str(e)}")
      return None
    
  # Connect to Google Cloud SQL on production
  connector = Connector()

  conn = connector.connect(
    os.getenv("INSTANCE_CONNECTION_NAME", ""), 
    "pg8000",
    user=os.getenv("DB_USER"), 
    db=os.getenv("DB_NAME"), 
    password=os.getenv("DB_PASSWORD")
  )

  return conn


def list_tables():
  conn = get_db_connection()
  if not conn:
    return None

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
    conn = get_db_connection()
    if not conn:
      return None
    
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
  conn = get_db_connection()
  if not conn:
    return None
  
  cur = conn.cursor()
  result = []
  for table in tables:
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}';")
    result.append(cur.fetchall())
  return result
