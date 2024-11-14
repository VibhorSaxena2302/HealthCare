import streamlit as st
import blog, login_signup, chatbot, userprofile, personalized_plan, dashboard, schedules, depression, iesr, ptsd, EmpathAI2
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

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    # Sidebar menu
    st.sidebar.title("Menu")

    if st.session_state['logged_in']:
        # Logged-in menu
        menu = ["Profile", "Dashboard", "Personalized Plan", "Schedules", "Create Blog", "View Blogs", "Chatbot", "CBT_Depression", "CBT_IES-R", "CBT_PTSD", "Granny", "Open Workout Assistant", "Logout"]
        choice = st.sidebar.radio("Navigation", menu, key='logged_in_menu')

        if choice == "Profile":
            userprofile.profile_page()
        elif choice == "Dashboard":
            dashboard.dashboard_page()
        elif choice == "Personalized Plan":
            personalized_plan.personalized_plan_page()
        elif choice == "Schedules":
            schedules.schedules_page()
        elif choice == "Create Blog":
            blog.create_blog()
        elif choice == "View Blogs":
            blog.view_blogs()
        elif choice == "Chatbot":
            chatbot.chatbot_page()
        elif choice == "CBT_Depression":
            depression.page()
        elif choice == "CBT_IES-R":
            iesr.page()
        elif choice == "CBT_PTSD":
            ptsd.page()
        elif choice == "Granny":
            EmpathAI2.page()
        elif choice == "Open Workout Assistant":
            open_external_link("http://localhost:8080/")
        elif choice == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['username'] = None
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
