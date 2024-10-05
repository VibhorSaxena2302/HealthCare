import streamlit as st
from sqlalchemy.orm import Session
from db_setup import UserHealthData, SessionLocal
import pandas as pd
import plotly.express as px

def dashboard_page():
    st.subheader("Your Health Dashboard")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    with SessionLocal() as db:
        health_data = db.query(UserHealthData).filter(UserHealthData.user_id == st.session_state['user_id']).order_by(UserHealthData.timestamp.asc()).all()

        if health_data:
            data = {
                'Timestamp': [hd.timestamp for hd in health_data],
                'Weight': [hd.weight for hd in health_data],
                'BMI': [hd.bmi for hd in health_data],
                'Body Fat': [hd.body_fat for hd in health_data],
                'Muscle Mass': [hd.muscle_mass for hd in health_data],
                'BMR': [hd.bmr for hd in health_data],
                'Bone Mass': [hd.bone_mass for hd in health_data],
                'Neck Circumference': [hd.neck_circumference for hd in health_data],
                'Waist Circumference': [hd.waist_circumference for hd in health_data],
                'Hip Circumference': [hd.hip_circumference for hd in health_data],
            }
            df = pd.DataFrame(data)

            # Melt DataFrame
            df_melted = df.melt('Timestamp', var_name='Metric', value_name='Value')

            # Plot with Plotly
            fig = px.line(df_melted, x='Timestamp', y='Value', color='Metric', markers=True, title='Health Metrics Over Time')
            fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metrics')

            st.plotly_chart(fig)

            # Display data table
            st.write("### Detailed Health Data")
            st.dataframe(df.set_index('Timestamp'))
        else:
            st.info("No health data available. Please update your profile to add health data.")
