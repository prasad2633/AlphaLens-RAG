from fastapi import FastAPI
from main import main
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    conversation_id: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/query")
def query(data: QueryRequest):
    answer = main(data.query, data.conversation_id)
    return {"answer": answer}
