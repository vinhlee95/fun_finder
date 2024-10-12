from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from agent import execute_query

app = FastAPI()

class QueryRequest(BaseModel):
    input: str

def preprocess_input(input_str: str) -> str:
    # Add your preprocessing logic here
    return input_str.strip()

@app.get("/available-slots")
def query(
    startHour: str = Query(..., example="18"), 
    endHour: str = Query(..., example="22"),
    date: str = Query(..., example="2024-10-18"),
    court_name: str = Query(..., example="Tennismesta"),
):
    try:
        # cleaned_input = preprocess_input(request.input)
        cleaned_input = f"""
          Are there any available hours {date} from {startHour}-{endHour} in {court_name} courts? 
          Give me the results with this format: date - hour - court_id - court_name. 
          Show the result as a table in the terminal.
        """
        
        result = execute_query(cleaned_input)
        return {"result": result.get("output")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))