from fastapi import APIRouter, Path, status, HTTPException
from prisma import Prisma
from models import PostCreate,PostResponse

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