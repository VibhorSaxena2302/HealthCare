import streamlit as st
from datetime import datetime
import random

def diary_app():
    # CSS for custom styling with Google Fonts
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap');

            .title {
                font-family: 'Indie Flower', cursive;
                color: #6D6875;
                font-size: 3em;
                text-align: left;
            }
            .date, .day, .dear-diary {
                font-family: 'Indie Flower', cursive;
                color: #B5838D;
                font-size: 1.8em;
                text-align: left;
                margin-top: 10px;
            }
            .entry, .gratitude-section, .prompt-section {
                font-family: 'Indie Flower', cursive;
                color: #4A4E69;
                font-size: 1.2em;
                margin-top: 20px;
            }
            .diary-space, .gratitude-space, .prompt-space {
                border: 2px dashed #4A4E69;
                border-radius: 10px;
                padding: 20px;
                background-color: #F7EDE2;
                font-family: 'Indie Flower', cursive;
                color: #4A4E69;
            }
            .save-button {
                background-color: #B5838D;
                color: white;
                font-size: 1.2em;
                border-radius: 10px;
                width: 100%;
                height: 50px;
                font-family: 'Indie Flower', cursive;
            }
            .save-button:hover {
                background-color: #6D6875;
            }
        </style>
    """, unsafe_allow_html=True)

    # Displaying the title
    st.markdown("<div class='title'>My Diary</div>", unsafe_allow_html=True)

    # Date and Day display
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_day = datetime.now().strftime("%A")
    st.markdown(f"<div class='date'>Date: {current_date}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='day'>Day: {current_day}</div>", unsafe_allow_html=True)

    # Dear Diary greeting
    st.markdown("<div class='dear-diary'>Dear Diary,</div>", unsafe_allow_html=True)

    # Expanded list of random prompts
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

    # Diary entry input
    st.markdown("<div class='entry'>What would you like to share today?</div>", unsafe_allow_html=True)
    entry = st.text_area("", placeholder="Write your thoughts here...", height=200, label_visibility="collapsed")

    # Gratitude Section
    st.markdown("<div class='gratitude-section'>Gratitude Section</div>", unsafe_allow_html=True)
    gratitude = st.text_area("What are you grateful for today?", placeholder="List things you are grateful for...", height=100, key="gratitude")


    # Save button
    if st.button("Save Entry", key="save", help="Click to save your diary entry"):
        st.markdown("<div class='entry'>Entry saved! 💖</div>", unsafe_allow_html=True)

    
    # Prompt Section
    st.markdown("<div class='prompt-section'>Need some inspiration? Here's a prompt for you:</div>", unsafe_allow_html=True)

    # Select a random prompt
    selected_prompt = random.choice(prompts)
    st.markdown(f"<div class='prompt-space'>{selected_prompt}</div>", unsafe_allow_html=True)