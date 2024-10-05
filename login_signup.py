import streamlit as st
import bcrypt
from sqlalchemy.orm import Session
from db_setup import User, SessionLocal, UserHealthData
from datetime import datetime
import math

import streamlit as st
import bcrypt
from sqlalchemy.orm import Session
from db_setup import User, SessionLocal, UserHealthData
from datetime import datetime
import math

def signup():
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    # Basic fields
    height = st.number_input("Height (in cm)", min_value=0.0, format="%.2f")
    weight = st.number_input("Weight (in kg)", min_value=0.0, format="%.2f")
    age = st.number_input("Age", min_value=0, format="%d")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    goal = st.text_input("Goal (e.g., Lose weight, Gain muscle)")
    medical_history = st.text_area("Medical History")

    # Additional health measurements
    st.write("**Additional Health Measurements (Optional but recommended):**")
    neck_circumference = st.number_input("Neck Circumference (cm)", min_value=0.0, format="%.2f")
    waist_circumference = st.number_input("Waist Circumference (cm)", min_value=0.0, format="%.2f")
    if gender == "Female":
        hip_circumference = st.number_input("Hip Circumference (cm)", min_value=0.0, format="%.2f")
    else:
        hip_circumference = 0.0
    muscle_mass = st.number_input("Muscle Mass (kg)", min_value=0.0, format="%.2f")
    bone_mass = st.number_input("Bone Mass (kg)", min_value=0.0, format="%.2f")

    if st.button("Sign Up"):
        if password == confirm_password and username:
            with SessionLocal() as db:
                # Check if username already exists
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    st.error("Username already exists. Please choose a different username.")
                else:
                    user = User(
                        username=username,
                        password=password,
                        height=height,
                        weight=weight,
                        age=age,
                        gender=gender,
                        goal=goal,
                        medical_history=medical_history
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)

                    # Calculate BMI
                    if height > 0 and weight > 0:
                        bmi = weight / ((height / 100) ** 2)
                    else:
                        bmi = None

                    # Calculate Body Fat Percentage using U.S. Navy Method
                    if gender == "Male" and neck_circumference > 0 and waist_circumference > 0 and height > 0:
                        body_fat = 86.010 * math.log10(waist_circumference - neck_circumference) - 70.041 * math.log10(height) + 36.76
                    elif gender == "Female" and neck_circumference > 0 and waist_circumference > 0 and hip_circumference > 0 and height > 0:
                        body_fat = 163.205 * math.log10(waist_circumference + hip_circumference - neck_circumference) - 97.684 * math.log10(height) - 78.387
                    else:
                        body_fat = None

                    # Calculate BMR using Mifflin-St Jeor Equation
                    if height > 0 and weight > 0 and age > 0:
                        if gender == "Male":
                            bmr = 10 * weight + 6.25 * height - 5 * age + 5
                        elif gender == "Female":
                            bmr = 10 * weight + 6.25 * height - 5 * age - 161
                        else:
                            bmr = None
                    else:
                        bmr = None

                    # Create a new health data record
                    new_health_data = UserHealthData(
                        user_id=user.id,
                        height=height,
                        weight=weight,
                        bmi=bmi,
                        body_fat=body_fat,
                        muscle_mass=muscle_mass if muscle_mass > 0 else None,
                        bmr=bmr,
                        bone_mass=bone_mass if bone_mass > 0 else None,
                        neck_circumference=neck_circumference if neck_circumference > 0 else None,
                        waist_circumference=waist_circumference if waist_circumference > 0 else None,
                        hip_circumference=hip_circumference if hip_circumference > 0 else None,
                        timestamp=datetime.utcnow()
                    )
                    db.add(new_health_data)
                    db.commit()
                    st.success("Account created successfully!")
        else:
            st.error("Passwords do not match or username is missing")

# Login function
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            if user and user.password == password:
                st.success(f"Welcome {username}!")
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user.id
                st.session_state['username'] = user.username
            else:
                st.error("Invalid username or password")


