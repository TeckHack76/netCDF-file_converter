from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase


# Connect to your SQLite DB
db = SQLDatabase.from_uri("sqlite:///argo.db")

# Load LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create chain
chain = create_sql_query_chain(llm, db)

# Ask a question
user_question = "Show me band1 data"
sql = chain.invoke({"question": user_question})

print("Generated SQL:", sql)
