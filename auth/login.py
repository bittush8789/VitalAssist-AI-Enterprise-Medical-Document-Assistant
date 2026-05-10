import streamlit as st
from auth.password_handler import verify_password
from database.db import SessionLocal
from database.models import User

def login_ui():
    st.markdown('<h2 style="text-align: center;">Member Login</h2>', unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="e.g. doctor@vitalassist.ai")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            db = SessionLocal()
            user = db.query(User).filter(User.email == email).first()
            db.close()
            
            if user and verify_password(password, user.hashed_password):
                st.session_state.authenticated = True
                st.session_state.user_role = user.role
                st.session_state.user_email = user.email
                st.success(f"Welcome back, {user.name}!")
                st.rerun()
            else:
                st.error("Invalid email or password")
