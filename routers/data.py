from fastapi import APIRouter, Path, status, HTTPException
from prisma import Prisma
from models import PostCreate,PostResponse
import pandas as pd
from func import calculate_moving_averages,calculate_performance, generate_signals
from typing import List

router = APIRouter()

@router.get("/data",response_model=List[PostResponse])
def get_posts():
    db=Prisma()
    db.connect()
    posts=db.post.find_many(order={'datetime': 'desc'})
    response = [
        PostResponse(
            id=post.id,
            datetime=post.datetime,
            open=float(round(post.open, 2)),
            high=float(round(post.high, 2)),
            low=float(round(post.low, 2)),
            close=float(round(post.close, 2)),
            volume=post.volume
        )
        for post in posts
    ]
    db.disconnect()
    return response

@router.post("/data",response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(create_data:PostCreate):
    db=Prisma()
    db.connect()
    post=db.post.create(data=create_data.model_dump(exclude_none=True))
    db.disconnect()

    return post


@router.get("/strategy/performance")
def strategy():
    db=Prisma()
    db.connect()

    posts=db.post.find_many(order={'datetime': 'desc'})
    
    response = [
        PostResponse(
            id=post.id,
            datetime=post.datetime,
            open=float(round(post.open, 2)),
            high=float(round(post.high, 2)),
            low=float(round(post.low, 2)),
            close=float(round(post.close, 2)),
            volume=post.volume
        )
        for post in posts
    ]
    df= pd.DataFrame([post.dict() for post in response])
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    df = df.sort_index(ascending=True)

    

    df = calculate_moving_averages(df)
    df = generate_signals(df)

    df = df.sort_index(ascending=True)

    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df = calculate_moving_averages(df)
    df = generate_signals(df)

    performance = calculate_performance(df)

    db.disconnect()
    
    return {"strategy": "Moving Average Crossover", "performance": performance}
