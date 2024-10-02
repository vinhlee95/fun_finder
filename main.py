from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from datetime import datetime, timedelta

from dotenv import load_dotenv
import pytz

from db.db import describe_tables_tool, list_tables, run_query_tool

load_dotenv()

llm = ChatOpenAI()

from langchain.tools import tool
@tool()
def get_next_weekday(phrase: str):
    """
    Return the date for the specified weekday phrase (e.g., "this Friday", "next Tuesday")
    in the format "YYYY-MM-DD" in EET timezone.
    """
    eet = pytz.timezone('Europe/Helsinki')
    today = datetime.now(eet)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    parts = phrase.split()
    if len(parts) != 2 or parts[0] not in ["this", "next"] or parts[1] not in weekdays:
        raise ValueError("Invalid phrase. Please use format 'this <weekday>' or 'next <weekday>'.")

    target_weekday = parts[1]
    target_weekday_index = weekdays.index(target_weekday)
    days_ahead = target_weekday_index - today.weekday()

    if parts[0] == "this":
        if days_ahead < 0:  # Target day already happened this week
            days_ahead += 7
    elif parts[0] == "next":
        if days_ahead <= 0:  # Target day already happened this week or is today
            days_ahead += 7

    next_weekday = today + timedelta(days=days_ahead)
    return next_weekday.strftime('%Y-%m-%d')


tables = list_tables()

prompt = ChatPromptTemplate(
  messages=[
    SystemMessage(content=
      f"You are an AI having access to a PostgreSQL database having following tables: {tables}. \n"
      "Do not make any assumption about the tables. \n"
      "Instead always try to use 'describe_tables_tool' to get schema of relevant tables \n"
      "before you try to figure out the query. \n"
      "Also, if a query is to filter by court_name, always use LIKE operator instead of =. \n"
      "remember to use % for wildcard search."
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    # agent_scratchpad is specific, kinda a simple form of memorising 
    # the output of the tool in the chain
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ],
  input_variables=[],
)

tools = [run_query_tool, describe_tables_tool, get_next_weekday]

agent = OpenAIFunctionsAgent(
  llm=llm,
  prompt=prompt,
  tools=tools,
)

agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True,
)

agent_executor.run(
  """
    Are there any available hours on this Friday after 6PM at "Olari" court? 
    Give me the results with this format: date - hour - court_id - court_name. 
    
    Show the result as a table in the terminal.
  """)
