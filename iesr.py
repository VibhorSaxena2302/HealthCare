import streamlit as st
import cohere

def page():
    # Initialize Cohere API
    cohere_client = cohere.Client('cYQPGLpHoYcpz74KloJi3NlyqRiSVtF6JkXvJUyY')  # Replace with your actual API key

    # Function to generate summary
    def generate_summary(observations, score):
        prompt = f"Based on the following observations from a mental health assessment:\n\n{observations}\n\nThe total score is: {score}\n\nGenerate a summary of the patient's mental health."
        
        response = cohere_client.generate(
            prompt=prompt,
            max_tokens=500, 
            temperature=0.7,
            k=0,
            p=0.75
        )
        
        return response.generations[0].text.strip()

    test_style = """
    <style>
    [data-testid="stApp"] {
        background-image: url("https://thumbs.dreamstime.com/z/mint-green-gradient-background-abstract-striped-background-light-mint-green-gradient-background-abstract-striped-background-189963480.jpg"); /* Path to your image */
        background-size: cover; /* Scales the image to cover the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
        }

            h1 {    
        color: black;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 20px;  
    }

    .question-title {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
    }


    .custom-text {
            color: black;
            font-size: 2em;  /* Equivalent to h2 size */
        }


    .summary-box {
        background-color: rgba(237,249,243, 0.3);
        padding: 20px;
        border-radius: 10px;
        margin: auto;
        width: 90%;
        text-align: left;
    }
    
    </style>
    """
    st.markdown(test_style, unsafe_allow_html=True)
    st.title("Revised Impact of Event Scale (IES-R)")

    questions = [
        {
            "question": "Any reminder of the event brought back feelings about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I woke up in the night",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Other things kept making me think about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I felt irritable and angry",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I avoided letting myself get upset when I thought about it or was reminded of it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I thought about it when I didn’t mean to",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I felt as if it hadn’t happened or wasn’t real",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I stayed away from reminders of it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Pictures about it popped into my mind",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I was jumpy and easily startled",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I tried not to think about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I was aware that I still had a lot of feelings about it, but I didn’t deal with them",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "My feelings about it were kind of numb",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I felt as if I was back at the time of the event",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I had trouble falling asleep",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I had waves of strong feelings about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I tried to remove it from my memory",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I had trouble concentrating",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Reminders of it caused me to have physical reactions, such as sweating, trouble breathing, nausea, or a pounding heart",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I had dreams about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I was watchful and on-guard",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "I tried not to talk about it",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        }
    ]

    def calculate_score(responses):
        score = 0
        for i, response in enumerate(responses):
            for option in questions[i]["options"]:
                if option["option"] == response:
                    score += option["weight"]
                    break
        return score


    responses = []
    for i, question in enumerate(questions):
    # Display the question inside the container using HTML to control layout
        st.markdown(f'<div class="question-title">Question {i + 1}: {question["question"]}</div>', unsafe_allow_html=True)
    
        # Display the selectbox within the container
        response = st.selectbox(
            "Your response:", 
            [option["option"] for option in question["options"]],
            key=f"q{i}"
        )
        responses.append(response)
        st.write("\n")

    # End the container for this question

    total_score = calculate_score(responses)
        
    if st.button("Submit"):
            
        st.write("Your total score is:", total_score)
        if total_score >= 0 and total_score <= 20:
            st.write("Your symptoms indicate low PTSD.")
        elif total_score >= 21 and total_score <= 40:
            st.write("Your symptoms indicate moderate PTSD.")
        else:
            st.write("Your symptoms indicate severe PTSD.")
        
    if st.button("Generate Summary"):
        summary = generate_summary("\n".join(responses), total_score)
                
            # Display summary in Streamlit
        st.markdown('<div class="custom-text"><b>### Summary of Patients Mental Health</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-box"><b>{summary}</b></div>', unsafe_allow_html=True)