from pydantic import BaseModel
from datetime import date

class FoodEntryCreate(BaseModel):
    date: date
    item_name: str
    prepared_qty: float
    consumed_qty: float

class FoodEntryOut(BaseModel):
    id: int
    date: date
    item_name: str
    prepared_qty: float
    consumed_qty: float
    wastage: float

    class Config:
        orm_mode = True
