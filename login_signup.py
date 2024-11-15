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
from db_setup import UserType

def signup():
    st.subheader("Create New Account")
    user_type = st.selectbox("I am a:", ["User", "Doctor"])
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    age = st.number_input("Age", min_value=0, format="%d")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone_number = st.text_input("Your WhatsApp Number (with country code, e.g., +1234567890)")
    
    if user_type == "User":
        # Basic fields
        user_type = "Patient"
        height = st.number_input("Height (in cm)", min_value=0.0, format="%.2f")
        weight = st.number_input("Weight (in kg)", min_value=0.0, format="%.2f")
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
    elif user_type == "Doctor":
        hospital = st.text_input("Hospital")
        contact_mail = st.text_input("Contact Email")
        specialty = st.text_input("Specialty")
        bio = st.text_area("Bio")

    if st.button("Sign Up"):
        if password == confirm_password and username:
            with SessionLocal() as db:
                # Check if username already exists
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    st.error("Username already exists. Please choose a different username.")
                else:
                    if user_type == "Patient":
                        user = User(
                            username=username,
                            password=password,
                            user_type=UserType.patient,
                            # Patient-specific fields
                            height=height,
                            weight=weight,
                            age=age,
                            gender=gender,
                            goal=goal,
                            medical_history=medical_history,
                            phone_number=phone_number
                        )
                        # Add health data if needed
                    elif user_type == "Doctor":
                        user = User(
                            username=username,
                            password=password,
                            age=age,
                            gender=gender,
                            hospital=hospital,
                            contact_mail=contact_mail,
                            phone_number=phone_number,
                            user_type=UserType.doctor,
                            specialty=specialty,
                            bio=bio
                        )
                    db.add(user)
                    db.commit()
                    db.refresh(user)

                    if user_type == "Patient":
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
            st.error("Passwords do not match or username or phone number is missing")

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
                st.session_state['user_type'] = user.user_type.value
            else:
                st.error("Invalid username or password")


