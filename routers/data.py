from fastapi import APIRouter, Path, status, HTTPException
from prisma import Prisma
from models import PostCreate,PostResponse
import pandas as pd
from func import calculate_moving_averages,calculate_performance, generate_signals

router = APIRouter()

@router.get("/data",response_model=PostResponse)
def get_posts():
    db=Prisma()
    db.connect()
    posts=db.post.find_many()
    db.disconnect()

    return posts

@router.post("/data",response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(create_data:PostCreate):
    db=Prisma()
    db.connect()
    post=db.post.create(data=create_data.model_dump(exclude_none=True))
    db.disconnect()

    return post


@router.get("/strategy/performance")
def strategy_performance():
    db=Prisma()
    db.connect()
    records = db.post.find_many(order={'datetime': 'asc'})

    df = pd.DataFrame(records)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    
    df = calculate_moving_averages(df)
    df = generate_signals(df)
    performance = calculate_performance(df)

    db.disconnect()

    return {"strategy": "Moving Average Crossover", "performance": performance}
