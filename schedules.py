# schedules.py

import streamlit as st
from sqlalchemy.orm import Session
from db_setup import User, UserSchedule, SessionLocal
from datetime import datetime, timedelta, time
import pandas as pd

def schedules_page():
    st.subheader("Your Schedules")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    if st.session_state.get('user_type') != 'patient':
        st.warning("Only patients can access this page.")
        return

    with SessionLocal() as db:
        user_id = st.session_state['user_id']
        user = db.query(User).filter(User.id == user_id).first()

        if user:

            st.info("""
                **Important:** To receive notifications on your WhatsApp number, you need to send a message to **+1 415 523 8886** with the text **"join connected-wealth"**.

                This will opt you into the WhatsApp sandbox environment.
            """)

            st.write("**Add a New Schedule:**")

            label = st.text_input("Label (e.g., Take medicine, Do yoga)")
            schedule_date = st.date_input("Start Date", value=datetime.now().date())
            times_input = st.text_input("Time (Enter time in HH:MM format, separated by commas, e.g., 09:00,12:00,17:00)")
            phone_number = user.phone_number
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
                        user_id=user_id,
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
            st.write("**Your Upcoming Schedules:**")

            # Fetch user's schedules
            schedules = db.query(UserSchedule).filter(UserSchedule.user_id == user_id).order_by(UserSchedule.schedule_date.asc()).all()

            if schedules:
                for sched in schedules:
                    recurrence = " (Daily)" if sched.is_recurring else ""
                    st.write(f"- **{sched.label}** on {sched.schedule_date.strftime('%Y-%m-%d')}{recurrence} at {sched.times} to {sched.phone_number}")
                    if st.button(f"Delete '{sched.label}'", key=f"del_{sched.id}"):
                        db.delete(sched)
                        db.commit()
                        st.success(f"Deleted schedule '{sched.label}'")
            else:
                st.info("You have no upcoming schedules.")
        else:
            st.error("User not found.")
