from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor

from dotenv import load_dotenv

from db.db import describe_tables_tool, list_tables, run_query_tool

load_dotenv()

llm = ChatOpenAI()


tables = list_tables()

prompt = ChatPromptTemplate(
  messages=[
    SystemMessage(content=
      f"You are an AI having access to a PostgreSQL database having following tables: {tables}. \n"
      "Do not make any assumption about the tables. \n"
      "Instead always try to use 'describe_tables_tool' to get schema of relevant tables \n"
      "before you try to figure out the query."
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    # agent_scratchpad is specific, kinda a simple form of memorising 
    # the output of the tool in the chain
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ],
  input_variables=[],
)

tools = [run_query_tool, describe_tables_tool]

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
    Are there any available hours in the next 2 days at "Smash Olari" court? 
    Give me the results with this format: date - hour - court_id - court_name
  """)