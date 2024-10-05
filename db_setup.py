from sqlalchemy import Float, create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://default:EuSoWVmj4f3M@ep-broad-wind-a1jdgsck-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require&connect_timeout=15"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define User table
class User(Base):
    __tablename__ = 'gfg_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    medical_history = Column(Text, nullable=True)
    age = Column(Integer, nullable=True)
    goal = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    health_data = relationship('UserHealthData', back_populates='user', cascade='all, delete-orphan')
    schedules = relationship('UserSchedule', back_populates='user', cascade='all, delete-orphan')

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

# Create the tables in the database
Base.metadata.create_all(engine)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
