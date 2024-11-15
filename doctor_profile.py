import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, SessionLocal

def doctor_profile():
    st.header("Doctor Profile")

    user_id = st.session_state['user_id']
    with SessionLocal() as db:
        doctor = db.query(User).filter(User.id == user_id).first()
        if doctor:
            st.write("**Username:**", doctor.username)
            st.write("**Phone Number:**", doctor.phone_number)
            st.write("**Age:**", doctor.age)
            st.write("**Gender:**", doctor.gender)
            st.write("**Hospital:**", doctor.hospital)     
            st.write("**Contact Email:**", doctor.contact_mail) 
            st.write("**Specialty:**", doctor.specialty)
            st.write("**Bio:**", doctor.bio)

            st.subheader("Update Profile")
            phone_number = st.text_input("Phone Number", value=doctor.phone_number)
            age = st.number_input("Age", min_value=0, value=doctor.age or 0, format="%d")
            gender_options = ["Male", "Female", "Other"]
            gender = st.selectbox("Gender", gender_options, index=gender_options.index(doctor.gender) if doctor.gender else 0)
            hospital = st.text_input("Hospital", value=doctor.hospital or "") 
            contact_mail = st.text_input("Contact Email", value=doctor.contact_mail or "")  
            specialty = st.text_input("Specialty", value=doctor.specialty)
            bio = st.text_area("Bio", value=doctor.bio)

            if st.button("Update Profile"):
                doctor.phone_number = phone_number
                doctor.age = age
                doctor.gender = gender
                doctor.hospital = hospital
                doctor.contact_mail = contact_mail
                doctor.specialty = specialty
                doctor.bio = bio
                db.commit()
                st.success("Profile updated successfully!")
        else:
            st.error("Doctor not found")
