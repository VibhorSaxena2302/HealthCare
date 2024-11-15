import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, UserHealthData, SessionLocal, PatientDoctorAssociation, Appointment, UserType
from datetime import datetime
import math

def view_doctors():
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
    st.header("Available Doctors")

    with SessionLocal() as db:
        doctors = db.query(User).filter(User.user_type == UserType.doctor).all()
        if doctors:
            for doctor in doctors:
                st.subheader(f"Dr. {doctor.username}")
                st.write(f"**Specialty:** {doctor.specialty}")
                st.write(f"**Bio:** {doctor.bio}")
                st.write(f"**Hospital:** {doctor.hospital or 'N/A'}")
                st.write(f"**Contact Email:** {doctor.contact_mail or 'N/A'}")
                st.write("---")
        else:
            st.info("No doctors found.")

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
            phone_number = st.text_input("Phone Number", value=user.phone_number)
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
            muscle_mass = st.number_input("Muscle Mass (%)", min_value=0.0, value=latest_health_data.muscle_mass or 0.0, format="%.2f")
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
                user.phone_number = phone_number
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

def manage_doctor_requests():
    st.header("My Doctors and Appointments")

    user_id = st.session_state['user_id']
    with SessionLocal() as db:
        # Fetch accepted doctor associations
        accepted_associations = db.query(PatientDoctorAssociation).filter(
            PatientDoctorAssociation.patient_id == user_id,
            PatientDoctorAssociation.status == 'Accepted'
        ).all()

        if accepted_associations:
            st.subheader("Your Associated Doctors and Appointments:")
            for assoc in accepted_associations:
                # Fetch doctor information
                doctor = db.query(User).filter(User.id == assoc.doctor_id).first()
                if doctor:
                    st.write(f"**Dr. {doctor.username}**")
                    st.write(f"Specialty: {doctor.specialty}")
                    st.write(f"Phone Number: {doctor.phone_number}")
                    st.write(f"Bio: {doctor.bio}")

                    # Fetch upcoming appointments with this doctor
                    appointments = db.query(Appointment).filter(
                        Appointment.patient_id == user_id,
                        Appointment.doctor_id == doctor.id,
                        Appointment.schedule_datetime >= datetime.now()
                    ).order_by(Appointment.schedule_datetime.asc()).all()

                    if appointments:
                        st.write(f"**Upcoming Appointments with Dr. {doctor.username}:**")
                        for appt in appointments:
                            st.write(f"- **Date and Time:** {appt.schedule_datetime.strftime('%Y-%m-%d %H:%M')}")
                            st.write(f"  **Status:** {appt.status}")
                            if appt.video_call_link:
                                st.write(f"  **Video Call Link:** [Join Video Call]({appt.video_call_link})")
                                if st.button(f"Join Video Call ({appt.schedule_datetime.strftime('%Y-%m-%d %H:%M')})", key=f"join_{appt.id}"):
                                    open_external_link(appt.video_call_link)
                            st.write("---")
                    else:
                        st.write(f"No upcoming appointments with Dr. {doctor.username}.")
                        st.write("---")
                else:
                    st.error("Doctor not found.")
        else:
            st.info("You have no associated doctors.")

        st.header("Doctor Requests")
        # Fetch pending doctor requests
        pending_associations = db.query(PatientDoctorAssociation).filter(
            PatientDoctorAssociation.patient_id == user_id,
            PatientDoctorAssociation.status == 'Pending'
        ).all()
        if pending_associations:
            for assoc in pending_associations:
                doctor = db.query(User).filter(User.id == assoc.doctor_id).first()
                if doctor:
                    st.write(f"Dr. {doctor.username} has requested to add you as a patient.")
                    col1, col2 = st.columns(2)
                    # Accept button
                    with col1:
                        if st.button(f"Accept Dr. {doctor.username}", key=f"accept_{assoc.id}"):
                            assoc.status = 'Accepted'
                            db.commit()
                            st.success(f"You have accepted the request from Dr. {doctor.username}.")
                    # Reject button
                    with col2:
                        if st.button(f"Reject Dr. {doctor.username}", key=f"reject_{assoc.id}"):
                            # Delete the association upon rejection
                            db.delete(assoc)
                            db.commit()
                            st.success(f"You have rejected the request from Dr. {doctor.username}.")
                else:
                    st.error("Doctor not found.")
        else:
            st.info("No pending doctor requests.")
    
    st.write('---')

    view_doctors()

def open_external_link(url):
    """
    Opens the given URL in a new browser tab.
    """
    # Use Streamlit's components to open the link
    import streamlit.components.v1 as components
    components.html(
        f"""
        <script>
        window.open("{url}", "_blank");
        </script>
        """,
        height=0,
        width=0
    )
