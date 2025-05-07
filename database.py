from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///./database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Extrato(Base):
    __tablename__ = "extratos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, index=True)
    tipo = Column(String, index=True)
    valor = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)
