from fastapi import FastAPI
from pydantic import BaseModel

from search import SearchSystem

app = FastAPI()

system = SearchSystem()

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(req: QueryRequest):
    return system.query(req.query)

@app.get("/cache/stats")
def stats():
    return system.cache.stats()

@app.delete("/cache")
def clear():
    system.cache.clear()
    return {"message": "cache cleared"}
