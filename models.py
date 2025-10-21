from pydantic import BaseModel, condecimal
from datetime import datetime

DecimalType = condecimal(max_digits=10, decimal_places=2)


class PostBase(BaseModel):
    open: DecimalType
    high: DecimalType
    low: DecimalType
    close: DecimalType
    volume: int

class PostCreate(BaseModel):
    open: DecimalType
    high: DecimalType
    low: DecimalType
    close: DecimalType
    volume: int

class PostResponse(PostBase):
    id: int
    datetime:datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    class Config:
        from_attributes = True 

