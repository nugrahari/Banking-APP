from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB.USER}:{settings.DB.PASSWORD}@{settings.DB.HOST}/{settings.DB.DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def session() -> SessionLocal:
    new_session = SessionLocal()
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()
