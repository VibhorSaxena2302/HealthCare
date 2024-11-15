import streamlit as st
from datetime import datetime
from db_setup import SessionLocal, DiaryEntry
import random

prompts = [
    "Write about a happy memory from childhood.",
    "Describe your perfect day from start to finish.",
    "What are three things you love about yourself?",
    "Write a letter to someone you admire.",
    "What is something new you learned today?",
    "List three goals you want to achieve this month.",
    "Describe a recent accomplishment you are proud of.",
    "Write about a time you helped someone and how it made you feel.",
    "What are some things that make you feel calm and relaxed?",
    "Describe your favorite place in the world and why it’s special.",
    "Write about a book, movie, or song that changed your perspective.",
    "What’s a lesson you’ve learned recently?",
    "Who is someone you are grateful for, and why?",
    "Describe something you're looking forward to.",
    "Write about a person who inspires you and what you admire about them.",
    "What’s a challenge you faced recently, and how did you overcome it?",
    "If you could have any superpower, what would it be and why?",
    "List five things that make you happy.",
    "Write about a dream you had recently.",
    "What are some habits you'd like to build?",
    "Describe a place you want to visit and why.",
    "What are three things you're grateful for today?",
    "What is something you want to learn or try this year?",
    "Write about a funny moment that happened to you.",
    "What is something you’re proud of that you don’t often talk about?"
]

def diary_entry_page():
    st.title("My Diary")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    if st.session_state.get('user_type') != 'patient':
        st.warning("Only patients can access this page.")
        return

    with SessionLocal() as db:
        # Check if user has already created an entry today
        user_id = st.session_state['user_id']
        today = datetime.utcnow().date()
        existing_entry = db.query(DiaryEntry).filter(
            DiaryEntry.user_id == user_id,
            DiaryEntry.timestamp >= datetime(today.year, today.month, today.day)
        ).first()

        if existing_entry:
            st.subheader("Today's Entry")
            st.write(f"**Date:** {existing_entry.timestamp.strftime('%Y-%m-%d')}")
            st.write(f"**Body:** {existing_entry.body}")
            st.write(f"**Gratefulness:** {existing_entry.gratefulness}")
            st.write(f"**Visible to Doctor:** {'Yes' if existing_entry.visible_to_doctor else 'No'}")
        else:
            st.subheader("Create a New Diary Entry")
            
            # Input fields for new diary entry
            body = st.text_area("Body", value='Dear Diary, ')
            gratefulness = st.text_input("What are you grateful for today?")
            visible_to_doctor = st.checkbox("Allow associated doctor to view this entry")

            st.write("Need some inspiration? Here's a prompt for you:")
            inspiration_prompt = random.choice(prompts)
            st.markdown(
                f"""
                <div style="border: 1px dashed #ccc; padding: 10px; background-color: #f77168; border-radius: 5px;">
                    <i>{inspiration_prompt}</i>
                </div><br>
                """, unsafe_allow_html=True
            )
            
            if st.button("Save Entry"):
                if body:
                    # Create a new diary entry
                    new_entry = DiaryEntry(
                        user_id=user_id,
                        body=body,
                        gratefulness=gratefulness,
                        visible_to_doctor=visible_to_doctor
                    )
                    db.add(new_entry)
                    db.commit()
                    st.success("Diary entry saved successfully!")
                else:
                    st.warning("Please fill in the body.")

        st.write("---")

        # Display past entries
        st.subheader("Past Entries")
        past_entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == user_id).order_by(DiaryEntry.timestamp.desc()).all()
        for entry in past_entries:
            st.write(f"**Date:** {entry.timestamp.strftime('%Y-%m-%d')}")
            st.write(f"**Body:** {entry.body}")
            st.write(f"**Gratefulness:** {entry.gratefulness}")
            st.write(f"**Visible to Doctor:** {'Yes' if entry.visible_to_doctor else 'No'}")

            if st.button(f"Toggle Visibility", key=f"toggle_{entry.id}"):
                entry.visible_to_doctor = not entry.visible_to_doctor
                db.commit()
                st.success(f"Diary entry visibility updated to {'Visible' if entry.visible_to_doctor else 'Hidden'}.")
                
            st.write("---")
