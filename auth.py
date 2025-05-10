import streamlit_authenticator as stauth
import LoginController as LoginController

# Carregar dados do banco
data = LoginController.loadall()
if data:
    names = data[0]
    users = data[1]
    passwords = data[2]

# Criar dicionário de credenciais no formato correto
credentials = {
    "usernames": {
        users[i]: {
            "email": "",
            "name": names[i],
            "password": passwords[i]
        } for i in range(len(users))
    }
}

# Inicializar o authenticator
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='some_cookie_name',
    cookie_key='some_key',
    cookie_expiry_days=30
)

