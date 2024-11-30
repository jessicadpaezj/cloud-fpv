import sqlalchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker

db = declarative_base()

def connect_db() -> sqlalchemy.engine.base.Engine:
    
    db_host = "34.95.252.108"
    db_user = "postgres"
    db_pass = "$'khs7QF`nykVDF5"
    db_name = "fpv-database"
    db_port = "5432"

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        )
    )
    return pool

engine = connect_db()
db_session = sessionmaker(bind=engine)
db_session = db_session()

class Video(db):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=True)
    time_stamp = Column(DateTime, nullable=True)
    path_folder = Column(String(1000), nullable=True)
    status = Column(String(255), nullable=True)
    user_id = Column(Integer)