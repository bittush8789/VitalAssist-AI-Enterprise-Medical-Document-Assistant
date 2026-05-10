import streamlit as st
from auth.password_handler import get_password_hash
from database.db import SessionLocal
from database.models import User

def register_ui():
    st.markdown('<h2 style="text-align: center;">Create Account</h2>', unsafe_allow_html=True)
    with st.form("register_form"):
        name = st.text_input("Full Name", placeholder="e.g. Dr. John Doe")
        email = st.text_input("Email", placeholder="e.g. john.doe@vitalassist.ai")
        password = st.text_input("Password", type="password", placeholder="Create a strong password")
        role = st.selectbox("Select Your Role", ["Doctor", "Insurance Officer", "Admin", "HR"])
        submit = st.form_submit_button("Register")
        
        if submit:
            db = SessionLocal()
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                st.error("User already exists!")
            else:
                new_user = User(
                    name=name,
                    email=email,
                    hashed_password=get_password_hash(password),
                    role=role
                )
                db.add(new_user)
                db.commit()
                st.success("Account created! Please log in.")
            db.close()
