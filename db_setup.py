from sqlalchemy import Float, create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import Enum
import enum 

DATABASE_URL = "DATABASE_URL"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_size=10, pool_pre_ping=True)
Base = declarative_base()

class UserType(enum.Enum):
    patient = "patient"
    doctor = "doctor"

# Define User table
class User(Base):
    __tablename__ = 'gfg_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    user_type = Column(Enum(UserType), default=UserType.patient)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    phone_number = Column(String)

    #Patient
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    medical_history = Column(Text, nullable=True)
    goal = Column(String, nullable=True)

    #Doctor
    specialty = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    hospital = Column(String, nullable=True) 
    contact_mail = Column(String, nullable=True)

    health_data = relationship('UserHealthData', back_populates='user', cascade='all, delete-orphan')
    schedules = relationship('UserSchedule', back_populates='user', cascade='all, delete-orphan')
    diary_entries = relationship('DiaryEntry', back_populates='user', cascade='all, delete-orphan')

    # Doctor-patient association
    patients = relationship(
        'PatientDoctorAssociation',
        back_populates='doctor',
        foreign_keys='PatientDoctorAssociation.doctor_id',
        cascade='all, delete-orphan'
    )
    doctors = relationship(
        'PatientDoctorAssociation',
        back_populates='patient',
        foreign_keys='PatientDoctorAssociation.patient_id',
        cascade='all, delete-orphan'
    )

class PatientDoctorAssociation(Base):
    __tablename__ = 'patient_doctor_association'
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('gfg_users.id'))
    doctor_id = Column(Integer, ForeignKey('gfg_users.id'))
    status = Column(String, default='Pending')  # e.g., 'Pending', 'Accepted', 'Rejected'

    patient = relationship('User', foreign_keys=[patient_id], back_populates='doctors')
    doctor = relationship('User', foreign_keys=[doctor_id], back_populates='patients')

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('gfg_users.id'))
    doctor_id = Column(Integer, ForeignKey('gfg_users.id'))
    schedule_datetime = Column(DateTime, nullable=False)
    video_call_link = Column(String, nullable=True)
    status = Column(String, default='Scheduled')

    patient = relationship('User', foreign_keys=[patient_id])
    doctor = relationship('User', foreign_keys=[doctor_id])

class UserHealthData(Base):
    __tablename__ = 'user_health_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('gfg_users.id'))
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    body_fat = Column(Float)
    muscle_mass = Column(Float)
    bmr = Column(Float)
    bone_mass = Column(Float)
    neck_circumference = Column(Float)
    waist_circumference = Column(Float)
    hip_circumference = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='health_data')

class UserSchedule(Base):
    __tablename__ = 'user_schedules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('gfg_users.id'))
    label = Column(String, nullable=False)
    schedule_date = Column(DateTime, nullable=False)  # Date only
    times = Column(String, nullable=False)  # Comma-separated times (HH:MM format)
    phone_number = Column(String, nullable=False)
    is_recurring = Column(Boolean, default=False)  # Repeat every day or not

    user = relationship('User', back_populates='schedules')

class DiaryEntry(Base):
    __tablename__ = 'diary_entries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('gfg_users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    body = Column(Text, nullable=False)
    gratefulness = Column(String, nullable=True)  
    visible_to_doctor = Column(Boolean, default=False) 

    user = relationship('User', back_populates='diary_entries')

# Define BlogPost table
class BlogPost(Base):
    __tablename__ = 'gfg_blog_posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('gfg_users.id'))
    author = relationship('User')
    likes = Column(Integer, default=0)
    image_url = Column(String, nullable=True)

    # Relationship with comments
    comments = relationship("Comment", back_populates="post", cascade="all, delete")

# Define Comment table
class Comment(Base):
    __tablename__ = 'gfg_comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('gfg_users.id'))
    post_id = Column(Integer, ForeignKey('gfg_blog_posts.id'))

    # Relationship to link the comment to its author and blog post
    author = relationship('User')
    post = relationship('BlogPost', back_populates='comments')

class UserStreak(Base):
    __tablename__ = 'user_streaks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('gfg_users.id'))
    streak_type = Column(String)  # 'steps' or 'calories'
    threshold = Column(Integer)  # The threshold value set by the user
    current_streak = Column(Integer, default=0)
    last_updated = Column(DateTime)
    user = relationship('User')

class UserStreakHistory(Base):
    __tablename__ = 'user_streak_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('gfg_users.id'))
    streak_type = Column(String)  # 'steps' or 'calories'
    date = Column(DateTime)
    value = Column(Integer)  # Steps or calories burned
    user = relationship('User')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
