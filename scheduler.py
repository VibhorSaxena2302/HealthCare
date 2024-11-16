from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session
from db_setup import UserSchedule, SessionLocal
from twilio.rest import Client
from datetime import datetime, timedelta
import os

TWILIO_ACCOUNT_SID = 'TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'TWILIO_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'TWILIO_WHATSAPP_NUMBER'

def send_whatsapp_message(to_number, message_body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{to_number}'
    )
    return message.sid


def check_and_send_messages():
    with SessionLocal() as db:
        # Get all schedules that are active today
        now = datetime.now()
        today = now.date()
        schedules = db.query(UserSchedule).filter(
            (UserSchedule.schedule_date <= now)
        ).all()

        for sched in schedules:
            # Convert schedule_date to date for comparison
            schedule_date_only = sched.schedule_date.date()
            times_list = [t.strip() for t in sched.times.split(',')]
            for t_str in times_list:
                scheduled_time = datetime.combine(schedule_date_only, datetime.strptime(t_str, "%H:%M").time())
                time_diff = (now - scheduled_time).total_seconds()

                # Check if the scheduled time is within the last minute and not in the future
                if 0 <= time_diff < 60:
                    try:
                        # Prepare the message
                        message_body = f"Reminder: {sched.label} scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M')}"
                        # Send the message
                        send_whatsapp_message(sched.phone_number, message_body)
                        print(f"Sent message to {sched.phone_number} for schedule '{sched.label}' at {t_str}")

                    except Exception as e:
                        print(f"Failed to send message for schedule '{sched.label}' at {t_str}: {e}")

            # If the schedule is not recurring and the date has passed, delete it
            if not sched.is_recurring and schedule_date_only < today:
                db.delete(sched)
                db.commit()
                print(f"Deleted non-recurring schedule '{sched.label}' after completion")
            elif sched.is_recurring:
                # Update the schedule date to today if it's in the past
                if schedule_date_only < today:
                    sched.schedule_date = datetime.combine(today, sched.schedule_date.time())
                    db.commit()
                    print(f"Updated recurring schedule '{sched.label}' date to today")

    print("Checked and sent messages at", datetime.now())

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Check every minute
    scheduler.add_job(check_and_send_messages, 'interval', minutes=1)
    try:
        print("Scheduler started...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass