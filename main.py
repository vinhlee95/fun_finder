from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent

from dotenv import load_dotenv

from db.db import describe_tables_tool, list_tables, run_query_tool
from tools import get_next_weekday

load_dotenv()

llm = ChatOpenAI()


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

agent = create_openai_functions_agent(
  llm=llm,
  prompt=prompt,
  tools=tools,
)

agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True,
)

agent_executor.invoke(
    {
        "input": """
          Are there any available hours today from 19-22 in Tennismesta courts? 
          Give me the results with this format: date - hour - court_id - court_name. 
          
          Show the result as a table in the terminal.
        """
    }
)
