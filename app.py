from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import execute_query

app = FastAPI()

class QueryRequest(BaseModel):
    input: str

def preprocess_input(input_str: str) -> str:
    # Add your preprocessing logic here
    return input_str.strip()

@app.get("/test")
def query():
    try:
        # cleaned_input = preprocess_input(request.input)
        cleaned_input = """
          Are there any available hours today from 19-22 in Tennismesta courts? 
          Give me the results with this format: date - hour - court_id - court_name. 
          Show the result as a table in the terminal.
        """
        
        result = execute_query(cleaned_input)
        return {"result": result.get("output")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))