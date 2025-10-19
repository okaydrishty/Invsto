from pydantic import BaseModel, condecimal
from datetime import datetime

DecimalType = condecimal(max_digits=10, decimal_places=2)


class PostBase(BaseModel):
    datetime: datetime
    open: DecimalType
    high: DecimalType
    low: DecimalType
    close: DecimalType
    volume: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    class Config:
        from_attributes = True 

