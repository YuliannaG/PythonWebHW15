from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.parser import get_db
from src.repository import news

# router = APIRouter()
router = APIRouter(prefix="/news", tags=["news"])


@router.get("/")
async def get_all_news(db: Session = Depends(get_db)):
    all_news = await news.get_all_news(db)
    return all_news
