import streamlit as st
from database import User, SessionLocal

@st.cache_data()
def loadall():
    db = SessionLocal()
    try:
        data = db.query(User).all()
        if data:
            datanames = [user.name for user in data]
            datausers = [user.username for user in data]
            datapasswords = [user.hashed_password for user in data]
            return datanames, datausers, datapasswords
        else:
            return [], [], []
    finally:
        db.close()