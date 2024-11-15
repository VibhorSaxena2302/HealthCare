import streamlit as st
import blog, login_signup, chatbot, userprofile, personalized_plan, dashboard, schedules, depression, iesr, ptsd, doctor_profile, doctor_patients, diary_entry, empathAI
import streamlit.components.v1 as components 

def open_external_link(url):
    """
    Opens the given URL in a new browser tab.
    """
    # Inject JavaScript to open the link
    components.html(
        f"""
        <script>
        window.open("{url}", "_blank");
        </script>
        """,
        height=0,  # Minimal height since we don't need to display anything
        width=0
    )
    st.success(f"Opened the workout assistant: {url}")

def main():
    st.set_page_config(page_title="HealthCare", page_icon="🩺", layout="wide")
    st.title("HealthCare")

    for key in ['logged_in', 'user_id', 'user_type', 'username']:
        if key not in st.session_state:
            st.session_state[key] = None if key != 'logged_in' else False

    # Sidebar menu
    st.sidebar.title("Menu")

    if st.session_state['logged_in']:
        user_type = st.session_state.get('user_type', 'patient')

        if user_type == 'patient':
            # Logged-in menu
            menu = ["Profile", "Dashboard", "Doctors", "Personalized Plan", "Schedules", "Diary Entry", "Streak", "Create Blog", "View Blogs", "Chatbot", "EmpathicAI", "CBT_Depression", "CBT_IES-R", "CBT_PTSD", "Open Workout Assistant", "Logout"]
            choice = st.sidebar.radio("Navigation", menu, key='logged_in_menu')

            if choice == "Profile":
                userprofile.profile_page()
            elif choice == "Dashboard":
                dashboard.dashboard_page()
            elif choice == "Doctors":
                userprofile.manage_doctor_requests()
            elif choice == "Personalized Plan":
                personalized_plan.personalized_plan_page()
            elif choice == "Schedules":
                schedules.schedules_page()
            elif choice == "Diary Entry":
                diary_entry.diary_entry_page()
            elif choice == "Streak":
                dashboard.streak_page()
            elif choice == "Create Blog":
                blog.create_blog()
            elif choice == "View Blogs":
                blog.view_blogs()
            elif choice == "Chatbot":
                chatbot.chatbot_page()
            elif choice == "EmpathicAI":
                empathAI.page()
            elif choice == "CBT_Depression":
                depression.page()
            elif choice == "CBT_IES-R":
                iesr.page()
            elif choice == "CBT_PTSD":
                ptsd.page()
            elif choice == "Open Workout Assistant":
                open_external_link("http://localhost:8080/")
            elif choice == "Logout":
                st.session_state['logged_in'] = False
                st.session_state['user_id'] = None
                st.session_state['username'] = None
                st.session_state['user_type'] = None
                st.success("You have been logged out.")
        elif user_type == 'doctor':
            # Doctor menu
            menu = ["Profile", "Patients", "Create Blog", "View Blogs", "Chatbot", "Logout"]
            choice = st.sidebar.radio("Navigation", menu)

            if choice == "Profile":
                doctor_profile.doctor_profile()
            elif choice == "Patients":
                doctor_patients.doctor_patients_page()
            elif choice == "Create Blog":
                blog.create_blog()
            elif choice == "View Blogs":
                blog.view_blogs()
            elif choice == "Chatbot":
                chatbot.chatbot_page()
            elif choice == "Logout":
                st.session_state['logged_in'] = False
                st.session_state['user_id'] = None
                st.session_state['username'] = None
                st.session_state['user_type'] = None
                st.success("You have been logged out.")
    else:
        # Not logged-in menu
        menu = [
            "Login",
            "Signup",
            "View Blogs",
            "Chatbot"
        ]
        choice = st.sidebar.radio("Navigation", menu, key='not_logged_in_menu')

        if choice == "Login":
            login_signup.login()
        elif choice == "Signup":
            login_signup.signup()
        elif choice == "View Blogs":
            blog.view_blogs()
        elif choice == "Chatbot":
            chatbot.chatbot_page()

if __name__ == '__main__':
    main()
