import streamlit as st
st.set_page_config(page_title="LesionAI", layout="wide")

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from app import run_app

# Load config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator instance (before login)
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    preauthorized=False
)

# 👇 Logo + Login FORM (regroupés dans une colonne)
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo.png", width=300)
        name, authentication_status, username = authenticator.login("Login", "main")
        st.info("👋 Happy to see you on **LesionAI**, the AI-powered assistant for intraoral lesion detection.")
else:
    name, authentication_status, username = authenticator.login("Login", "main")

# 🔒 Login flow
if authentication_status is False:
    st.error("Incorrect username or password")
elif authentication_status:
    authenticator.logout("Logout", "main")
    st.success(f"Welcome {name} 👋")
    run_app(username)
