import streamlit as st
import streamlit_authenticator as stauth
import LoginController as LoginController

# Inicializar o estado da sessão se não existir
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None

# Carregar dados do banco
try:
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

        location = {
            "main": "main"
        }

        # Inicializar o authenticator
        authenticator = stauth.Authenticate(
            credentials=credentials,
            cookie_name='some_cookie_name',
            cookie_key='some_key',
            cookie_expiry_days=30
        )

        # Login
        name, authentication_status, username = authenticator.login("Login", location)

        # Atualizar o estado da sessão
        st.session_state["authentication_status"] = authentication_status
        st.session_state["name"] = name

        # Logout
        if st.session_state["authentication_status"]:
            test = authenticator.logout("Logout", location)
            st.write(f"Habemus *{st.session_state['name']}*!")
        elif st.session_state["authentication_status"] == False:
            st.error("Usuário ou senha inválida!")
        elif st.session_state["authentication_status"] == None:
            st.warning("Insira o Usuário e a senha.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
