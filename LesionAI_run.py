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

# Login box
name, authentication_status, username = authenticator.login("Login", "main")

# ✅ Logo et message affichés uniquement AVANT connexion
if authentication_status is None:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("assets/logo.png", width=450)
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("👋 Happy to see you on **LesionAI**, the AI-powered assistant for intraoral lesion detection.")

elif authentication_status is False:
    st.error("Incorrect username or password")

elif authentication_status:
    authenticator.logout("Logout", "main")
    st.success(f"Welcome {name} 👋")
    run_app(username)
