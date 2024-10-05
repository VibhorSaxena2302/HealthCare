import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, UserHealthData, SessionLocal
from datetime import datetime
import math

def profile_page():
    st.subheader("Your Profile")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    with SessionLocal() as db:
        user = db.query(User).filter(User.id == st.session_state['user_id']).first()
        latest_health_data = db.query(UserHealthData).filter(UserHealthData.user_id == user.id).order_by(UserHealthData.timestamp.desc()).first()

        if user:
            st.write("**Update Your Profile Information:**")

            # Existing fields
            username = st.text_input("Username", value=user.username, disabled=True)
            height = st.number_input("Height (in cm)", min_value=0.0, value=user.height or 0.0, format="%.2f")
            weight = st.number_input("Weight (in kg)", min_value=0.0, value=user.weight or 0.0, format="%.2f")
            age = st.number_input("Age", min_value=0, value=user.age or 0, format="%d")
            gender_options = ["Male", "Female", "Other"]
            gender = st.selectbox("Gender", gender_options, index=gender_options.index(user.gender) if user.gender else 0)
            goal = st.text_input("Goal", value=user.goal or "")
            medical_history = st.text_area("Medical History", value=user.medical_history or "")

            # Additional inputs
            neck_circumference = st.number_input("Neck Circumference (cm)", min_value=0.0, value=latest_health_data.neck_circumference or 0.0, format="%.2f")
            waist_circumference = st.number_input("Waist Circumference (cm)", min_value=0.0, value=latest_health_data.waist_circumference or 0.0, format="%.2f")
            if gender == "Female":
                hip_circumference = st.number_input("Hip Circumference (cm)", min_value=0.0, value=latest_health_data.hip_circumference or 0.0, format="%.2f")
            else:
                hip_circumference = 0.0
            muscle_mass = st.number_input("Muscle Mass (kg)", min_value=0.0, value=latest_health_data.muscle_mass or 0.0, format="%.2f")
            bone_mass = st.number_input("Bone Mass (kg)", min_value=0.0, value=latest_health_data.bone_mass or 0.0, format="%.2f")

            if st.button("Update Profile"):
                # Calculate BMI
                bmi = weight / ((height / 100) ** 2) if height > 0 else None

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

                # Update User data
                user.height = height
                user.weight = weight
                user.age = age
                user.gender = gender
                user.goal = goal
                user.medical_history = medical_history

                # Create new health data record
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
                st.success("Profile and health data updated successfully!")
        else:
            st.error("User not found.")
