from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from datetime import datetime
from db.database import Base

class TrendSource(Base):
    __tablename__ = "trend_sources"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    source       = Column(String(50))
    title        = Column(String(500))
    url          = Column(String(1000))
    score        = Column(Integer)
    collected_at = Column(DateTime)
    created_at   = Column(DateTime, default=datetime.now)

class TrendAnalysis(Base):
    __tablename__ = "trend_analysis"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    date       = Column(Date, unique=True)
    keywords   = Column(Text)
    summary    = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(Integer)
    title       = Column(String(500))
    content     = Column(Text)
    status      = Column(String(20), default="draft")
    posted_at   = Column(DateTime)
    tistory_id  = Column(String(100))
    created_at  = Column(DateTime, default=datetime.now)