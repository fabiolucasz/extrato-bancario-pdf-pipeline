from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime



# Configurações do banco de dados
DATABASE_URL = "sqlite:///./database.db"

# Configurar engine com pool de conexões
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Extrato(Base):
    __tablename__ = "extratos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, index=True)
    tipo = Column(String, index=True)
    valor = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))



# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)