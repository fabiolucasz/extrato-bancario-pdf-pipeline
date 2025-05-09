import streamlit as st
from database import User, SessionLocal


#resgatar da database todos os nomes,usuarios e senhas
#comparar com os dados do usuario que esta tentando logar
#se os dados estiverem corretos, redirecionar para a pagina de dashboard
#se os dados estiverem incorretos, mostrar mensagem de erro

    
#comment def checklogin
#def checklogin(username, password):
#    count = db.cursor.execute("SELECT name FROM users WHERE username = '" + username + "' AND hashed_password = '" + password + "'").rowcount
#    user = count.fetchone()
#    if user:
#        return True, user[0]
#    else:
#        return False, None

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
    #count = db.cursor.execute("SELECT name, username, hashed_password FROM users").rowcount
    #data = count.fetchall()
    
    #datanames = [name[0].strip() for name in data]  
    #datausers = [user[1].strip() for user in data]
    #datapasswords = [password[2].strip() for password in data]
    #if datanames:
        #return datanames, datausers, datapasswords
    #else:
        #return None


