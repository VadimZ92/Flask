import atexit
from sqlalchemy import  Column, String, Integer, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = "postgresql://app:1234@127.0.0.1:5431/flask"


engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)


atexit.register(engine.dispose)

class Advertising(Base):

    __tablename__ = "app_advertising"

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    user = Column(String, nullable=False, index=True)

Base.metadata.create_all(bind=engine)