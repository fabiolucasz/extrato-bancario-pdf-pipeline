import streamlit as st
from database import User, SessionLocal

st.title("Seja bem-vindo!!")


session = SessionLocal()
username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar"):
    user = session.query(User).filter_by(username=username).first()
    if username == user.username and password == user.hashed_password:
        st.success("Login realizado com sucesso!")
        st.session_state['user_id'] = user.id
        st.session_state['username'] = user.username
    else:
        st.error("Usuário ou senha inválidos!")
