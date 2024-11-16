import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, UserHealthData, SessionLocal
from llm_model import llm
from datetime import datetime
import math

# Initialize your LLM model
chatbot = llm()

def personalized_plan_page():
    test_style = """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://i.pinimg.com/736x/86/86/a6/8686a6cc18f857fcef1b9a782bdc4d30.jpg"); /* Path to your image */
        background-size: cover;  /*Scales the image to cover the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
    }
    
    </style>
    """
    st.markdown(test_style, unsafe_allow_html=True)
    st.subheader("Get Your Personalized Plan")

    # Check if the user is logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to access this page.")
        return

    # Retrieve user data from the database
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == st.session_state['user_id']).first()
        latest_health_data = db.query(UserHealthData).filter(UserHealthData.user_id == user.id).order_by(UserHealthData.timestamp.desc()).first()

        if user:
            st.write("**Please confirm or update your profile data:**")

            # Editable fields
            age = st.number_input("Age", value=user.age or 0)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user.gender) if user.gender else 0)
            height = st.number_input("Height (in cm)", value=user.height or 0.0)
            weight = st.number_input("Weight (in kg)", value=user.weight or 0.0)
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

            if st.button("Update Profile Data"):
                with SessionLocal() as db:
                    user_db = db.query(User).filter(User.id == st.session_state['user_id']).first()
                    user_db.age = age
                    user_db.gender = gender
                    user_db.height = height
                    user_db.weight = weight
                    user_db.goal = goal
                    user_db.medical_history = medical_history

                    # Calculate BMI
                    bmi = weight / ((height / 100) ** 2) if height > 0 else None

                    # Calculate Body Fat Percentage
                    if gender == "Male" and neck_circumference > 0 and waist_circumference > 0 and height > 0:
                        body_fat = 86.010 * math.log10(waist_circumference - neck_circumference) - 70.041 * math.log10(height) + 36.76
                    elif gender == "Female" and neck_circumference > 0 and waist_circumference > 0 and hip_circumference > 0 and height > 0:
                        body_fat = 163.205 * math.log10(waist_circumference + hip_circumference - neck_circumference) - 97.684 * math.log10(height) - 78.387
                    else:
                        body_fat = None

                    # Calculate BMR
                    if height > 0 and weight > 0 and age > 0:
                        if gender == "Male":
                            bmr = 10 * weight + 6.25 * height - 5 * age + 5
                        elif gender == "Female":
                            bmr = 10 * weight + 6.25 * height - 5 * age - 161
                        else:
                            bmr = None
                    else:
                        bmr = None

                    # Create new health data record
                    new_health_data = UserHealthData(
                        user_id=user_db.id,
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
                    st.success("Profile data and health metrics updated successfully!")

            missing_data = []
            if not age:
                missing_data.append("Age")
            if not gender:
                missing_data.append("Gender")
            if not height:
                missing_data.append("Height")
            if not weight:
                missing_data.append("Weight")
            if not goal:
                missing_data.append("Goal")
            if not medical_history:
                missing_data.append("Medical History")

            if missing_data:
                st.error(f"The following profile data is missing: {', '.join(missing_data)}")
                st.info("Please update your profile before generating a personalized plan.")
                return

            # Display user's current data
            st.write("**Your Profile Data:**")
            st.write(f"- **Username:** {user.username}")
            st.write(f"- **Age:** {age}")
            st.write(f"- **Gender:** {gender}")
            st.write(f"- **Height:** {height} cm")
            st.write(f"- **Weight:** {weight} kg")
            st.write(f"- **Goal:** {goal}")
            st.write(f"- **Medical History:** {medical_history}")
            st.write(f"- **Muscle Mass:** {muscle_mass} kg")
            st.write(f"- **Bone Mass:** {bone_mass} kg")
            st.write(f"- **Body Fat Percentage:** {latest_health_data.body_fat or 'N/A'}%")

            st.write("---")

            # Allow the user to select the plan type
            plan_type = st.selectbox("Select Plan Type", ["Personalized Exercise Plan", "Personalized Diet Plan"])

            # Button to generate the plan
            if st.button("Generate Plan"):
                # Compose the prompt for the LLM
                prompt = f"""
                You are a certified health and fitness expert.

                Your task is to create a personalized {plan_type.lower()} that will help the individual achieve their goal: **{goal}**.

                Here are the individual's details:

                - **Username:** {user.username}
                - **Age:** {age}
                - **Gender:** {gender}
                - **Height:** {height} cm
                - **Weight:** {weight} kg
                - **Muscle Mass:** {muscle_mass} kg
                - **Bone Mass:** {bone_mass} kg
                - **Body Fat Percentage:** {latest_health_data.body_fat or 'N/A'}%
                - **Medical History:** {medical_history}

                **Requirements:**

                - Provide a detailed and safe plan tailored to the individual's needs.
                - Focus on strategies and recommendations that specifically address their goal of **{goal}**.
                - Include actionable steps, guidelines, and tips to help them effectively reach their goal.
                - Consider their medical history to ensure all recommendations are appropriate.

                Please present the plan in a clear and organized manner.
                """

                # Generate the plan using the LLM model
                with st.spinner("Generating your personalized plan..."):
                    plan = ""
                    for chunk in chatbot.stream_generate(prompt=prompt, tokens=3000):
                        plan += chunk

                # Display the generated plan
                st.subheader("Your Personalized Plan")
                st.write(plan)

        else:
            st.error("User not found.")