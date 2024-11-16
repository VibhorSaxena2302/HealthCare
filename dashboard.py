import math
import streamlit as st
from db_setup import UserHealthData, SessionLocal, UserStreak, UserStreakHistory, User
import pandas as pd
import plotly.express as px
import googleapiclient.discovery
import datetime
import google_auth_oauthlib 
from googleapiclient.errors import HttpError
import random
import colorsys

def generate_random_color():
    h, s, l = random.random(), 0.5 + random.random() / 2, 0.4 + random.random() / 5
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "rgb({},{},{})".format(int(r*255), int(g*255), int(b*255))

SCOPES = [
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
]

def get_user_credentials_fixed_port(scopes, client_id, client_secret, fixed_port=8500):
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    app_flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=scopes
    )

    return app_flow.run_local_server(host='localhost', port=fixed_port)

def authenticate_user():
    credentials = get_user_credentials_fixed_port(
        client_id="981259142195-vb5lfm4dogcg4qrl9gi83phhhh60dbls.apps.googleusercontent.com",
        client_secret="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",
        scopes=SCOPES,
    )
    st.session_state['credentials'] = credentials

def build_google_fit_service(credentials):
    service = googleapiclient.discovery.build(
        'fitness', 'v1', credentials=credentials)
    return service

def fetch_weight_data(service, start_time, end_time):
    data_source = "derived:com.google.weight:com.google.android.gms:merge_weight"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    weights = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                weight = field.get('fpVal')
                if weight:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    weights.append({'Timestamp': timestamp, 'Weight (kgs)': weight})
    return weights

def fetch_bmr_data(service, start_time, end_time):
    data_source = "derived:com.google.calories.bmr:com.google.android.gms:merged"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    vallist = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                val = field.get('fpVal')
                if val:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    vallist.append({'Timestamp': timestamp, 'Basal metabolic rate (BMR) (kcal per day)': val})
    return vallist

def fetch_calories_expanded_data(service, start_time, end_time):
    data_source = "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    vallist = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                val = field.get('fpVal')
                if val:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    vallist.append({'Timestamp': timestamp, 'Calories Burned (kcal)': val})
    return vallist

def fetch_heart_rate_bpm_data(service, start_time, end_time):
    data_source = "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    vallist = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                val = field.get('fpVal')
                if val:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    vallist.append({'Timestamp': timestamp, 'Heart Rate (bpm)': val})
    return vallist

def fetch_height_data(service, start_time, end_time):
    data_source = "derived:com.google.height:com.google.android.gms:merge_height"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    vallist = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                val = field.get('fpVal')
                if val:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    vallist.append({'Timestamp': timestamp, 'Height (meters)': val})
    return vallist

def fetch_body_fat_percentage_data(service, start_time, end_time):
    data_source = "derived:com.google.body.fat.percentage:com.google.android.gms:merged"

    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    request = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset)
    response = request.execute()

    vallist = []
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                val = field.get('fpVal')
                if val:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)
                    vallist.append({'Timestamp': timestamp, 'Body Fat Percentage': val*100})
    return vallist

def fetch_step_count_data(service, start_time, end_time):
    data_source = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
    dataset = f"{int(start_time.timestamp() * 1e9)}-{int(end_time.timestamp() * 1e9)}"

    response = service.users().dataSources().datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset).execute()

    steps_data = []
    
    if 'point' in response:
        for point in response['point']:
            for field in point['value']:
                steps = field.get('intVal')  # Get the integer value for steps
                if steps:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(point['startTimeNanos']) / 1e9)  # Convert from nanoseconds to seconds
                    steps_data.append({'Timestamp': timestamp, 'Steps': steps})
    
    return steps_data

def collect_google_fit_data(service):
    try:
        data_sources = service.users().dataSources().list(userId='me').execute()
        for data_source in data_sources.get('dataSource', []):
            print("Data Source ID:", data_source['dataStreamId'])
            print("Data Type:", data_source['dataType']['name'])
        # Define the time range (e.g., last 30 days)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=30)

        # Fetch data
        steps_data = fetch_step_count_data(service, start_time, end_time)
        weight_data = fetch_weight_data(service, start_time, end_time)
        bmr_data = fetch_bmr_data(service, start_time, end_time)
        calories_data = fetch_calories_expanded_data(service, start_time, end_time)
        heart_rate_data = fetch_heart_rate_bpm_data(service, start_time, end_time)
        height_data = fetch_height_data(service, start_time, end_time)
        body_fat_percentage_data = fetch_body_fat_percentage_data(service, start_time, end_time) 
        # Add more functions for other metrics if available

        # Convert to DataFrame
        df_steps = pd.DataFrame(steps_data)
        df_weight = pd.DataFrame(weight_data)
        df_bmr = pd.DataFrame(bmr_data)
        df_calories = pd.DataFrame(calories_data)
        df_heart_rate = pd.DataFrame(heart_rate_data)
        df_height = pd.DataFrame(height_data)
        df_body_fat = pd.DataFrame(body_fat_percentage_data)

        # Sort by Timestamp
        df_steps.sort_values('Timestamp', inplace=True)
        df_weight.sort_values('Timestamp', inplace=True)
        df_bmr.sort_values('Timestamp', inplace=True)
        df_calories.sort_values('Timestamp', inplace=True)
        df_heart_rate.sort_values('Timestamp', inplace=True)
        df_height.sort_values('Timestamp', inplace=True)
        df_body_fat.sort_values('Timestamp', inplace=True)

        return {'Steps': df_steps, 'Weight (kgs)': df_weight, 'Height (meters)':df_height, 'Basal metabolic rate (BMR) (kcal per day)':df_bmr, 'Calories Burned (kcal)':df_calories, 'Body Fat Percentage':df_body_fat, 'Heart Rate (bpm)':df_heart_rate}
    except:
        return {}

def dashboard_page():
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
    st.subheader("Your Health Dashboard")

    # Ensure user is logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    # Fetch data from your database (manually entered data)
    with SessionLocal() as db:
        health_data = db.query(UserHealthData).filter(
            UserHealthData.user_id == st.session_state['user_id']
        ).order_by(UserHealthData.timestamp.asc()).all()

        if health_data:
            data = {
                'Timestamp': [hd.timestamp for hd in health_data],
                'Weight': [hd.weight for hd in health_data],
                'Height': [hd.height for hd in health_data],
                'BMI': [hd.bmi for hd in health_data],
                'Body Fat': [hd.body_fat for hd in health_data],
                'Muscle Mass': [hd.muscle_mass for hd in health_data],
                'BMR': [hd.bmr for hd in health_data],
                'Bone Mass': [hd.bone_mass for hd in health_data],
                'Neck Circumference': [hd.neck_circumference for hd in health_data],
                'Waist Circumference': [hd.waist_circumference for hd in health_data],
                'Hip Circumference': [hd.hip_circumference for hd in health_data],
            }
            df_db = pd.DataFrame(data)
            df_db.sort_values('Timestamp', inplace=True)
        else:
            st.info("No health data available in the database.")
            df_db = pd.DataFrame()  # Empty DataFrame

    # Display manually entered data
    if not df_db.empty:
        # Melt DataFrame for plotting
        df_melted_db = df_db.melt('Timestamp', var_name='Metric', value_name='Value')

        # Plot with Plotly
        fig_db = px.line(
            df_melted_db,
            x='Timestamp',
            y='Value',
            color='Metric',
            markers=True,
            title='Manually Entered Health Metrics Over Time'
        )
        fig_db.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metrics')

        st.plotly_chart(fig_db)

        # Display data table
        st.write("#### Detailed Manually Entered Health Data")
        st.dataframe(df_db.set_index('Timestamp'))
    else:
        st.info("No manually entered health data to display.")

    # Option to authenticate with Google Fit
    st.write("---")
    st.write("### Connect with Google Fit to Get Additional Data")

    if 'credentials' in st.session_state and st.session_state['credentials']:
        try:
            service = googleapiclient.discovery.build('fitness', 'v1', credentials=st.session_state['credentials'])
            df_google_fit = collect_google_fit_data(service)
            st.write("### Your Google Fit Health Data")

            for df_key in df_google_fit.keys():
                df_melted_fit = df_google_fit[df_key].melt('Timestamp', var_name='Metric', value_name='Value')

                unique_metrics = df_melted_fit['Metric'].unique()

                color_sequence = [generate_random_color() for _ in unique_metrics]

                # Plot with Plotly
                fig_fit = px.line(
                    df_melted_fit,
                    x='Timestamp',
                    y='Value',
                    color='Metric',
                    markers=True,
                    title=df_key,
                    color_discrete_sequence=color_sequence
                )
                fig_fit.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metrics')

                st.plotly_chart(fig_fit)

                # Display data table
                st.write("#### Detailed Google Fit Health Data for", df_key)
                df_google_fit[df_key] = df_google_fit[df_key].sort_values(by='Timestamp', ascending=False)
                st.dataframe(df_google_fit[df_key].set_index('Timestamp'))
            
            gfit_weight_series = df_google_fit.get('Weight (kgs)', pd.DataFrame())
            gfit_height_series = df_google_fit.get('Height (meters)', pd.DataFrame())

            if not gfit_weight_series.empty and not gfit_height_series.empty:
                with SessionLocal() as db:
                    user = db.query(User).filter(User.id == st.session_state['user_id']).first()
                    latest_health_data = db.query(UserHealthData).filter(UserHealthData.user_id == user.id).order_by(UserHealthData.timestamp.desc()).first()

                    if user:
                        latest_weight = float(format(float(gfit_weight_series.iloc[-1]['Weight (kgs)'].max()), ".2f"))
                        latest_height = float(format(float(gfit_height_series.iloc[0]['Height (meters)'].max()), ".2f"))
                        print(latest_weight)
                        if latest_weight > 0 and latest_height > 0:
                            if latest_weight!=latest_health_data.weight or latest_height!=latest_health_data.height:
                                # Convert height from meters to cm
                                latest_height_cm = latest_height * 100

                                # Update user's height and weight
                                user.height = latest_height_cm
                                user.weight = latest_weight

                                # Recalculate BMI and Body Fat with updated values
                                bmi = latest_weight / ((latest_height_cm / 100) ** 2)

                                if user.gender == "Female":
                                    hip_circumference = st.number_input("Hip Circumference (cm)", min_value=0.0, value=latest_health_data.hip_circumference or 0.0, format="%.2f")
                                else:
                                    hip_circumference = 0.0

                                # Calculate Body Fat Percentage using U.S. Navy Method
                                if user.gender == "Male" and latest_health_data.neck_circumference > 0 and latest_health_data.waist_circumference > 0 and latest_height_cm > 0:
                                    body_fat = 86.010 * math.log10(latest_health_data.waist_circumference - latest_health_data.neck_circumference) - 70.041 * math.log10(latest_height_cm) + 36.76
                                elif user.gender == "Female" and latest_health_data.neck_circumference > 0 and latest_health_data.waist_circumference > 0 and hip_circumference > 0 and latest_height_cm > 0:
                                    body_fat = 163.205 * math.log10(latest_health_data.waist_circumference + hip_circumference - latest_health_data.neck_circumference) - 97.684 * math.log10(latest_height_cm) - 78.387
                                else:
                                    body_fat = None

                                # Calculate BMR using Mifflin-St Jeor Equation
                                if latest_height_cm > 0 and latest_weight > 0 and user.age > 0:
                                    if user.gender == "Male":
                                        bmr = 10 * latest_weight + 6.25 * latest_height_cm - 5 * user.age + 5
                                    elif user.gender == "Female":
                                        bmr = 10 * latest_weight + 6.25 * latest_height_cm - 5 * user.age - 161
                                    else:
                                        bmr = None
                                else:
                                    bmr = None

                                # Create new health data record with Google Fit data
                                new_health_data = UserHealthData(
                                    user_id=user.id,
                                    height=latest_height_cm,
                                    weight=latest_weight,
                                    bmi=bmi,
                                    body_fat=body_fat,
                                    muscle_mass=latest_health_data.muscle_mass if latest_health_data.muscle_mass > 0 else None,
                                    bmr=bmr,
                                    bone_mass=latest_health_data.bone_mass if latest_health_data.bone_mass > 0 else None,
                                    neck_circumference=latest_health_data.neck_circumference if latest_health_data.neck_circumference > 0 else None,
                                    waist_circumference=latest_health_data.waist_circumference if latest_health_data.waist_circumference > 0 else None,
                                    hip_circumference=hip_circumference if hip_circumference > 0 else None,
                                    timestamp=datetime.datetime.utcnow()
                                )
                                db.add(new_health_data)
                                db.commit()
                                st.success("Profile updated with Google Fit data successfully!")

        except HttpError as error:
            st.error(f"An error occured: {error}")
    else:
        # Button to authenticate with Google Fit
        st.button("Connect with Google fit", type="primary", on_click=authenticate_user)

def streak_page():
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
    st.subheader("Your Streaks")

    # Ensure user is logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("You need to log in to view this page.")
        return

    # Ensure user is authenticated with Google
    if 'credentials' not in st.session_state or not st.session_state['credentials']:
        st.warning("You need to connect with Google Fit to use this function.")
        if st.button("Connect with Google Fit", type="primary"):
            authenticate_user()
        return

    # Proceed if authenticated
    st.write("Select which streaks you want to track:")
    steps_streak = st.checkbox("Steps Goal Streak")
    calories_streak = st.checkbox("Calories Burned Goal Streak")

    streakval = 10000
    caloriesval = 500
    
    with SessionLocal() as db:
        user_id = st.session_state['user_id']

        if steps_streak:
            steps_streak_obj = db.query(UserStreak).filter_by(user_id=user_id, streak_type='steps').first()
            if steps_streak_obj != None and steps_streak_obj.threshold:
                streakval = steps_streak_obj.threshold
                
        if calories_streak:
            calories_streak_obj = db.query(UserStreak).filter_by(user_id=user_id, streak_type='calories').first()
            if calories_streak_obj != None and calories_streak_obj.threshold:
                caloriesval = calories_streak_obj.threshold    

    # Allow user to set threshold values
    if steps_streak:
        steps_threshold = st.number_input("Set your daily steps goal:", min_value=0, value=streakval, step=100)
    if calories_streak:
        calories_threshold = st.number_input("Set your daily calories burned goal (kcal):", min_value=0, value=caloriesval, step=10)

    if st.button("Update Streaks"):
        # Fetch data from Google Fit
        service = build_google_fit_service(st.session_state['credentials'])
        # Define the time range (e.g., last 30 days)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=30)

        # Fetch steps data
        steps_data = fetch_step_count_data(service, start_time, end_time)
        # Fetch calories data
        calories_data = fetch_calories_expanded_data(service, start_time, end_time)

        # Process and aggregate data per day
        df_steps = pd.DataFrame(steps_data)
        df_calories = pd.DataFrame(calories_data)

        # Aggregate steps per day
        if not df_steps.empty:
            df_steps['Date'] = df_steps['Timestamp'].dt.date
            steps_per_day = df_steps.groupby('Date')['Steps'].sum().reset_index()
        else:
            steps_per_day = pd.DataFrame()

        # Aggregate calories per day
        if not df_calories.empty:
            df_calories['Date'] = df_calories['Timestamp'].dt.date
            calories_per_day = df_calories.groupby('Date')['Calories Burned (kcal)'].sum().reset_index()
        else:
            calories_per_day = pd.DataFrame()

        # Initialize variables to hold current streak values
        current_steps_streak = None
        current_calories_streak = None

        # Update streaks
        with SessionLocal() as db:
            user_id = st.session_state['user_id']

            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)

            # Steps Streak
            if steps_streak:
                # Get or create UserStreak for steps
                steps_streak_obj = db.query(UserStreak).filter_by(user_id=user_id, streak_type='steps').first()
                if not steps_streak_obj:
                    steps_streak_obj = UserStreak(
                        user_id=user_id,
                        streak_type='steps',
                        threshold=steps_threshold,
                        current_streak=0,
                        last_updated=None
                    )
                    db.add(steps_streak_obj)
                    db.commit()
                    db.refresh(steps_streak_obj)

                # Update threshold if changed
                if steps_streak_obj.threshold != steps_threshold:
                    steps_streak_obj.threshold = steps_threshold

                # Get today's steps
                today_steps = steps_per_day[steps_per_day['Date'] == today]['Steps'].sum()
                if pd.isna(today_steps):
                    today_steps = 0

                # Get yesterday's steps (for streak continuation)
                yesterday_steps = steps_per_day[steps_per_day['Date'] == yesterday]['Steps'].sum()
                if pd.isna(yesterday_steps):
                    yesterday_steps = 0

                # Update streak regardless of last_updated
                if today_steps >= steps_threshold:
                    # Goal met today
                    if steps_streak_obj.last_updated == yesterday and yesterday_steps >= steps_threshold:
                        # Goal was met yesterday, continue streak
                        steps_streak_obj.current_streak += 1
                    else:
                        # Start new streak
                        steps_streak_obj.current_streak = 1
                else:
                    # Goal not met today, reset streak
                    steps_streak_obj.current_streak = 0

                # Update last_updated
                steps_streak_obj.last_updated = today
                db.commit()

                # Save or update today's steps in UserStreakHistory
                steps_history = db.query(UserStreakHistory).filter_by(
                    user_id=user_id, streak_type='steps', date=today).first()
                if steps_history:
                    steps_history.value = int(today_steps)
                else:
                    steps_history = UserStreakHistory(
                        user_id=user_id,
                        streak_type='steps',
                        date=today,
                        value=int(today_steps)
                    )
                    db.add(steps_history)
                db.commit()

                # Store current streak value before session closes
                current_steps_streak = steps_streak_obj.current_streak

            # Calories Streak
            if calories_streak:
                # Get or create UserStreak for calories
                calories_streak_obj = db.query(UserStreak).filter_by(user_id=user_id, streak_type='calories').first()
                if not calories_streak_obj:
                    calories_streak_obj = UserStreak(
                        user_id=user_id,
                        streak_type='calories',
                        threshold=calories_threshold,
                        current_streak=0,
                        last_updated=None
                    )
                    db.add(calories_streak_obj)
                    db.commit()
                    db.refresh(calories_streak_obj)

                # Update threshold if changed
                if calories_streak_obj.threshold != calories_threshold:
                    calories_streak_obj.threshold = calories_threshold

                # Get today's calories burned
                today_calories = calories_per_day[calories_per_day['Date'] == today]['Calories Burned (kcal)'].sum()
                if pd.isna(today_calories):
                    today_calories = 0

                # Get yesterday's calories burned
                yesterday_calories = calories_per_day[calories_per_day['Date'] == yesterday]['Calories Burned (kcal)'].sum()
                if pd.isna(yesterday_calories):
                    yesterday_calories = 0

                # Update streak regardless of last_updated
                if today_calories >= calories_threshold:
                    # Goal met today
                    if calories_streak_obj.last_updated == yesterday and yesterday_calories >= calories_threshold:
                        # Goal was met yesterday, continue streak
                        calories_streak_obj.current_streak += 1
                    else:
                        # Start new streak
                        calories_streak_obj.current_streak = 1
                else:
                    # Goal not met today, reset streak
                    calories_streak_obj.current_streak = 0

                # Update last_updated
                calories_streak_obj.last_updated = today
                db.commit()

                # Save or update today's calories burned in UserStreakHistory
                calories_history = db.query(UserStreakHistory).filter_by(
                    user_id=user_id, streak_type='calories', date=today).first()
                if calories_history:
                    calories_history.value = int(today_calories)
                else:
                    calories_history = UserStreakHistory(
                        user_id=user_id,
                        streak_type='calories',
                        date=today,
                        value=int(today_calories)
                    )
                    db.add(calories_history)
                db.commit()

                # Store current streak value before session closes
                current_calories_streak = calories_streak_obj.current_streak

        # Display streaks and plot graphs
        st.write("### Your Current Streaks:")
        if steps_streak:
            st.write(f"**Steps Goal Streak:** {current_steps_streak} days")
            # Fetch steps history
            with SessionLocal() as db:
                steps_history = db.query(UserStreakHistory).filter_by(
                    user_id=user_id, streak_type='steps'
                ).order_by(UserStreakHistory.date.asc()).all()
                if steps_history:
                    df_steps_history = pd.DataFrame({
                        'Date': [sh.date for sh in steps_history],
                        'Steps': [sh.value for sh in steps_history]
                    })
                    # Plot
                    fig_steps = px.line(df_steps_history, x='Date', y='Steps', title='Steps Over Time', markers=True)
                    fig_steps.add_hline(y=steps_threshold, line_dash="dash", line_color="red", annotation_text="Threshold")
                    st.plotly_chart(fig_steps)
        if calories_streak:
            st.write(f"**Calories Burned Goal Streak:** {current_calories_streak} days")
            # Fetch calories history
            with SessionLocal() as db:
                calories_history = db.query(UserStreakHistory).filter_by(
                    user_id=user_id, streak_type='calories'
                ).order_by(UserStreakHistory.date.asc()).all()
                if calories_history:
                    df_calories_history = pd.DataFrame({
                        'Date': [ch.date for ch in calories_history],
                        'Calories Burned': [ch.value for ch in calories_history]
                    })
                    # Plot
                    fig_calories = px.line(df_calories_history, x='Date', y='Calories Burned', title='Calories Burned Over Time', markers=True)
                    fig_calories.add_hline(y=calories_threshold, line_dash="dash", line_color="red", annotation_text="Threshold")
                    st.plotly_chart(fig_calories)