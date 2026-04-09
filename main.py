from db.database import engine, Base
from db import models

def init_db():
    print("DB 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ DB 테이블 생성 완료!")

if __name__ == "__main__":
    init_db()