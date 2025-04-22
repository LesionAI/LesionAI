import streamlit as st
st.set_page_config(page_title="LesionAI", layout="wide")

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from app import run_app

# Auth setup
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    preauthorized=False
)

# ✅ Logo affiché avant le formulaire de login
name, authentication_status, username = None, None, None
if "authentication_status" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo.png", width=350)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is None:
    st.info("👋 Happy to see you on **LesionAI**, the AI-powered assistant for intraoral lesion detection.")

elif authentication_status is False:
    st.error("Incorrect username or password")

elif authentication_status:
    authenticator.logout("Logout", "main")
    st.success(f"Welcome {name} 👋")
    run_app(username)
