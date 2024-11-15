import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, UserSchedule, PatientDoctorAssociation, SessionLocal, UserType, Appointment, DiaryEntry
from datetime import datetime
import uuid
from llm_model import llm

chatbot = llm()

def doctor_patients_page():
    st.header("Manage Patients")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in as a doctor to view this page.")
        return

    if st.session_state.get('user_type') != 'doctor':
        st.warning("You need to log in as a doctor to view this page.")
        return

    with SessionLocal() as db:
        doctor_id = st.session_state['user_id']
        doctor = db.query(User).filter(User.id == doctor_id).first()

        if doctor:
            # Get the list of patients associated with the doctor
            associations = db.query(PatientDoctorAssociation).filter(
                PatientDoctorAssociation.doctor_id == doctor_id,
                PatientDoctorAssociation.status == 'Accepted'
            ).all()
            patients = [assoc.patient for assoc in associations]

            st.subheader("My Patients")
            if patients:
                patient_options = {f"{patient.username} (ID: {patient.id})": patient for patient in patients}
                selected_patient_name = st.selectbox("Select a patient", list(patient_options.keys()))
                selected_patient = patient_options[selected_patient_name]

                st.write(f"Selected Patient: {selected_patient.username}")

                # Manage schedules for the selected patient
                manage_patient_schedules(selected_patient, db)

                # Manage appointments with the selected patient
                manage_patient_appointments(selected_patient, doctor_id, db)

                view_patient_diary_entries(selected_patient, db)
            else:
                st.info("You have no associated patients.")

            st.subheader("Add a Patient")
            # Allow doctor to send association requests to patients
            add_patient(doctor_id, db)
        else:
            st.error("Doctor not found.")

def add_patient(doctor_id, db):
    # Fetch all patients who are not already associated with the doctor
    existing_patient_ids = [
        assoc.patient_id for assoc in db.query(PatientDoctorAssociation).filter(
            PatientDoctorAssociation.doctor_id == doctor_id
        ).all()
    ]
    all_patients = db.query(User).filter(
        User.user_type == UserType.patient,
        ~User.id.in_(existing_patient_ids)
    ).all()

    patient_options = {f"{patient.username} (ID: {patient.id})": patient.id for patient in all_patients}
    if patient_options:
        selected_patient_name = st.selectbox("Select Patient to Add", list(patient_options.keys()))
        if st.button("Send Request"):
            selected_patient_id = patient_options[selected_patient_name]
            association = PatientDoctorAssociation(
                doctor_id=doctor_id,
                patient_id=selected_patient_id,
                status='Pending'
            )
            db.add(association)
            db.commit()
            st.success(f"Request sent to patient {selected_patient_name}.")
    else:
        st.write("No unassociated patients available.")

def manage_patient_schedules(patient, db):
    st.subheader(f"Schedules for {patient.username}")

    # Display patient's phone number
    if patient.phone_number:
        phone_number = patient.phone_number
        st.write(f"Patient's WhatsApp Number: {phone_number}")
    else:
        st.warning(f"{patient.username} has not provided a phone number.")
        phone_number = st.text_input("Patient's WhatsApp Number (with country code, e.g., +1234567890)")
        if st.button("Update Patient's Phone Number"):
            patient.phone_number = phone_number
            db.commit()
            st.success("Patient's phone number updated successfully!")

    st.write("**Add a New Schedule for Patient:**")

    label = st.text_input("Label (e.g., Take medicine, Do yoga)")
    schedule_date = st.date_input("Start Date", value=datetime.now().date())
    times_input = st.text_input("Times (Enter times in HH:MM format, separated by commas, e.g., 09:00,12:00,17:00)")
    is_recurring = st.checkbox("Repeat every day at these times")

    if st.button("Add Schedule"):
        if label and phone_number and times_input:
            # Validate times
            times_list = [t.strip() for t in times_input.split(',')]
            valid_times = []
            for t in times_list:
                try:
                    valid_time = datetime.strptime(t, "%H:%M").time()
                    valid_times.append(valid_time.strftime("%H:%M"))
                except ValueError:
                    st.error(f"Invalid time format: {t}. Please use HH:MM format.")
                    return

            # Store times as comma-separated string
            times_str = ','.join(valid_times)

            new_schedule = UserSchedule(
                user_id=patient.id,
                label=label,
                schedule_date=schedule_date,
                times=times_str,
                phone_number=phone_number,
                is_recurring=is_recurring
            )
            db.add(new_schedule)
            db.commit()
            st.success("Schedule added successfully!")
        else:
            st.error("Please fill in all required fields.")

    st.write("---")
    st.write(f"**Upcoming Schedules for {patient.username}:**")

    # Fetch patient's schedules
    schedules = db.query(UserSchedule).filter(UserSchedule.user_id == patient.id).order_by(UserSchedule.schedule_date.asc()).all()

    if schedules:
        for sched in schedules:
            recurrence = " (Daily)" if sched.is_recurring else ""
            st.write(f"- **{sched.label}** on {sched.schedule_date.strftime('%Y-%m-%d')}{recurrence} at {sched.times} to {sched.phone_number}")
            if st.button(f"Delete '{sched.label}'", key=f"del_{sched.id}"):
                db.delete(sched)
                db.commit()
                st.success(f"Deleted schedule '{sched.label}'")
    else:
        st.info(f"{patient.username} has no upcoming schedules.")

def manage_patient_appointments(patient, doctor_id, db):
    st.subheader(f"Appointments with {patient.username}")

    st.write("**Schedule a New Appointment:**")

    date = st.date_input("Appointment Date", key="appt_date", value=datetime.now().date())
    time_input = st.time_input("Appointment Time (Enter in HH:MM format, eg: (17:00)", key="appt_time")
    datetime_combined = datetime.combine(date, time_input)

    if st.button("Schedule Appointment"):
        # Generate a unique video call link
        room_name = str(uuid.uuid4())
        video_call_link = f"https://meet.jit.si/{room_name}"
        new_appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            schedule_datetime=datetime_combined,
            video_call_link=video_call_link,
            status='Scheduled'
        )
        db.add(new_appointment)
        db.commit()
        st.success(f"Appointment scheduled with {patient.username} on {datetime_combined}.")
        st.write(f"Video call link: {video_call_link}")

    st.write("---")
    st.write(f"**Upcoming Appointments with {patient.username}:**")

    # Fetch appointments
    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.patient_id == patient.id,
        Appointment.schedule_datetime >= datetime.now()
    ).order_by(Appointment.schedule_datetime.asc()).all()

    if appointments:
        for appt in appointments:
            st.write(f"- Appointment on {appt.schedule_datetime.strftime('%Y-%m-%d %H:%M')} - Status: {appt.status}")
            st.write(f"Video call link: {appt.video_call_link}")
            if st.button(f"Cancel Appointment on {appt.schedule_datetime}", key=f"cancel_{appt.id}"):
                db.delete(appt)
                db.commit()
                st.success(f"Appointment on {appt.schedule_datetime} canceled.")
    else:
        st.info(f"No upcoming appointments with {patient.username}.")

def view_patient_diary_entries(patient, db):
    st.subheader(f"Diary Entries for {patient.username}")

    # Fetch visible diary entries
    diary_entries = db.query(DiaryEntry).filter(
        DiaryEntry.user_id == patient.id,
        DiaryEntry.visible_to_doctor == True  # Only show entries marked as visible
    ).order_by(DiaryEntry.timestamp.desc()).all()

    if diary_entries:
        for entry in diary_entries:
            st.write(f"**Date:** {entry.timestamp.strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Body:** {entry.body}")
            st.write(f"**Gratefulness:** {entry.gratefulness}")

            # Generate Report Button
            if st.button("Generate Report", key=f"report_{entry.id}"):
                # Compose prompt for generating report based on diary entry
                prompt = f"""
                You are a certified mental health expert.

                Your task is to analyze the following diary entry and provide a professional report that gives insights into the patient's emotional and mental well-being.

                **Diary Entry:**
                {entry.body}

                **Details of the Patient:**
                - **Username**: {patient.username}
                - **Age**: {patient.age if patient.age else 'N/A'}
                - **Gender**: {patient.gender if patient.gender else 'N/A'}
                - **Height:** {patient.height} cm
                - **Weight:** {patient.weight} kg
                - **Medical History:** {patient.medical_history}
                - **Goal:** {patient.goal}
                
                **Requirements:**
                - Analyze the tone, mood, and emotions expressed in the entry.
                - Identify any signs of stress, happiness, or other emotional states.
                - Offer insights or suggestions that could be helpful for the patient's mental well-being based on the diary content.
                - Keep the report professional, empathetic, and focused on helping the doctor understand the patient’s mental state.

                Present the report in a clear and organized manner.
                """

                # Generate the report using the LLM model
                with st.spinner("Generating report..."):
                    report = ""
                    for chunk in chatbot.stream_generate(prompt=prompt, tokens=1000):
                        report += chunk

                # Display the generated report below the diary entry
                st.subheader("Generated Report")
                st.write(report)
    else:
        st.info(f"No diary entries from {patient.username} are visible to you.")

