from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI demo")
app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"], 
                   allow_methods=["*"], 
                   allow_headers=["*"])

class ItemIn(BaseModel):
    name: str = Field(..., min_length=1)
    path: str = Field(..., min_length=2, pattern=r"^(.*/)([^/]*)$")

class ItemOut(ItemIn):
    id: int

ITEMS: List[ItemOut] = [
    ItemOut(id=0, name="mars images 2020", path="path/to/mars"), 
    ItemOut(id=1, name="europa images 1987", path="path/to/europa"), 
    ItemOut(id=2, name="mars rover soil samples", path="path/to/rover/soilsamples")
]

# curl "http://127.0.0.1:8000/"
@app.get("/")
def root():
    return "Here's the FastAPI root"

# curl "http://127.0.0.1:8000/search/europa%20images%201987"
@app.get("/search/{item}")
def search(item: str):
    return {"message": f"You searched for: '{item}'"}

# curl "http://127.0.0.1:8000/all" or 
# curl "http://127.0.0.1:8000/all?limit=2"
@app.get("/all", response_model=List[ItemOut])
def list_all(limit: Optional[int] = Query(default=None, ge=1, le=100)):
    return ITEMS[:limit] if limit else ITEMS

""" 
curl -X POST "http://127.0.0.1:5000/new-item" \
     -H "Content-Type: application/json" \
     -d '{"name":"moon base schematics 2028","path":"path/to/moon/base/schematics"}'
"""
@app.post("/new-item", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    new_id = max(i.id for i in ITEMS) + 1 if ITEMS else 0
    new_item = ItemOut(id=new_id, **item.model_dump())
    ITEMS.append(new_item)
    return new_item

# run with: uvicorn fastapitest:app --reload
