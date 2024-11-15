import streamlit as st
import cohere

def page():
    # Initialize Cohere API
    cohere_client = cohere.Client('cYQPGLpHoYcpz74KloJi3NlyqRiSVtF6JkXvJUyY')  # Replace with your actual API key

    # Function to generate summary
    def generate_summary(observations, score):
        prompt = f"Based on the following observations from a mental health assessment:\n\n{observations}\n\nYou scored {score} on the PCL-5 questionnaire for PTSD. Based on the score, provide a summary of the implications of this score regarding potential PTSD symptoms and based on observation, write summary about patients mental health."
        
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
        background-image: url(https://thumbs.dreamstime.com/z/mint-green-gradient-background-abstract-striped-background-light-mint-green-gradient-background-abstract-striped-background-189963480.jpg"); /* Path to your image */
        background-size: cover; /* Scales the image to cover the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: 0% 30%; /* Centers the image */
        }

    .question-title {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
    }

    h1 {    
        color: black;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 20px;  
    }

    .custom-text {
            color: black;
            font-size: 2em;  /* Equivalent to h2 size */
        }


    .summary-box {
        background-color: rgba(183,253,219, 0.3);
        padding: 20px;
        border-radius: 10px;
        margin: auto;
        width: 90%;
        text-align: left;
    }
    
    </style>
    """
    st.markdown(test_style, unsafe_allow_html=True)
    st.title("PCL-5")
    st.write("Post-traumatic Stress Disorder Checklist DSM-5 Version")
    st.write("Instructions: Here is a list of problems that people sometimes experience after a really stressful event. Please read each statement carefully and check the box to indicate how much this problem has affected you in the last month.")

    questions = [
        {
            "question": "Repeated, distressing, involuntary memories of the stressful experience?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Repeated, distressing dreams of the stressful experience?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Suddenly feeling or acting as if the stressful experience were happening again?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Feeling very upset when something reminds you of the event?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Having strong physical reactions when something reminds you of the event (e.g., heart pounding, trouble breathing, sweating)?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Avoiding memories, thoughts, or feelings related to the event?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Avoiding external reminders (people, places, conversations, activities, objects) that remind you of the stressful experience?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Negative beliefs about yourself, others, or the world (e.g., 'I am bad,' 'I can't trust anyone,' 'The world is dangerous')?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Blaming yourself or others for the event or what happened after?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Having strong negative feelings such as fear, horror, anger, guilt, or shame?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Loss of interest in activities you used to enjoy?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Feeling distant or cut off from others?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Having trouble experiencing positive feelings (e.g., being unable to feel happiness or love for those close to you)?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Irritable behavior, angry outbursts, or acting aggressively?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Taking risks or engaging in behaviors that could put you in danger?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Being 'on guard,' watchful, or easily startled?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Having difficulty concentrating?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
                {"option": "Moderately", "weight": 2},
                {"option": "Quite a bit", "weight": 3},
                {"option": "Extremely", "weight": 4}
            ]
        },
        {
            "question": "Trouble falling asleep or staying asleep?",
            "options": [
                {"option": "Not at all", "weight": 0},
                {"option": "A little bit", "weight": 1},
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