from sqlalchemy.orm import Session

from src.models import News


async def get_all_news(db: Session):
    news = db.query(News).all()
    return news