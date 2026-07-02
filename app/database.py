from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from app.core.setting import DATABASE_URL
 

engine = create_engine(DATABASE_URL)
SessionLocal = Session(
    autocommit=False,
    autoflush=False,
    bind = engine
)

Base = declarative_base()