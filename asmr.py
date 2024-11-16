import streamlit as st

def page():
    # App title
    st.title("🧘 Meditation Therapy Videos")

    # Introduction
    st.write("""
    Explore a curated selection of meditation therapy videos to help you relax, de-stress, and find inner peace.
    """)

    # List of YouTube videos
    videos = [
        {"title": "10-Minute Guided Meditation for Relaxation", "url": "https://www.youtube.com/embed/inpok4MKVLM"},
        {"title": "30-Minute Deep Relaxation Meditation", "url": "https://www.youtube.com/embed/ZToicYcHIOU"},
        {"title": "Morning Meditation for Positive Energy", "url": "https://www.youtube.com/embed/1vx8iUvfyCY"},
        {"title": "Sleep Meditation for Calm and Rest", "url": "https://www.youtube.com/embed/z6X5oEIg6Ak"},
    ]

    # Display videos
    for video in videos:
        st.subheader(video["title"])
        st.video(video["url"])

    # Footer
    st.write("---")
    st.write("🌟 Find your calm and center with these meditation therapy videos!")