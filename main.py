from fastapi import FastAPI
from typing import Union
from prisma import Prisma
from routers import data
app=FastAPI()



app.include_router(data.router)