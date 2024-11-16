import streamlit as st
import cohere

def page():
    # Initialize Cohere API
    cohere_client = cohere.Client('COHERE_API')  # Replace with your actual API key

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
        background-size: cover;  /*Scales the image to cover the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
        }

    h4 {    
        color: black;
        font-size: 4rem;
        font-weight: bold;
    }

    .question-box {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 10px;
        padding: 10px;
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
    st.title("BDI-2 - Beck Depression Inventory")

    questions = [
        {
            "question": "Sadness",
            "options": [
                {"option": "I do not feel sad", "weight": 0},
                {"option": "I feel sad much of the time", "weight": 1},
                {"option": "I am sad all the time", "weight": 2},
                {"option": "I am so sad or unhappy that I can't stand it", "weight": 3}
            ]
        },
        {
            "question": "Pessimism",
            "options": [
                {"option": "I am not discouraged about my future", "weight": 0},
                {"option": "I feel more discouraged about my future than I used to", "weight": 1},
                {"option": "I do not expect things to work out for me", "weight": 2},
                {"option": "I feel my future is hopeless and will only get worse", "weight": 3}
            ]
        },
        {
            "question": "Past Failures",
            "options": [
                {"option": "I do not feel like a failure", "weight": 0},
                {"option": "I have failed more than I should have", "weight": 1},
                {"option": "As I look back, I see a lot of failures", "weight": 2},
                {"option": "I feel I am a complete failure as a person", "weight": 3}
            ]
        },
        {
            "question": "Loss of Pleasure",
            "options": [
                {"option": "I get as much pleasure as I ever did from things I enjoy", "weight": 0},
                {"option": "I don't enjoy things as much as I used to", "weight": 1},
                {"option": "I get very little pleasure from the things I used to enjoy", "weight": 2},
                {"option": "I can't get any pleasure from the things I used to enjoy", "weight": 3}
            ]
        },
        {
            "question": "Guilty Feelings",
            "options": [
                {"option": "I don't feel particularly guilty", "weight": 0},
                {"option": "I feel guilty over many things I have done or should have done", "weight": 1},
                {"option": "I feel guilty most of the time", "weight": 2},
                {"option": "I feel guilty all of the time", "weight": 3}
            ]
        },
        {
            "question": "Feeling Punished",
            "options": [
                {"option": "I don't feel I am being punished", "weight": 0},
                {"option": "I feel I may be punished", "weight": 1},
                {"option": "I expect to be punished", "weight": 2},
                {"option": "I feel I am being punished", "weight": 3}
            ]
        },
        {
            "question": "Self-Dislike",
            "options": [
                {"option": "I feel the same about myself as ever", "weight": 0},
                {"option": "I have lost confidence in myself", "weight": 1},
                {"option": "I am disappointed in myself", "weight": 2},
                {"option": "I dislike myself", "weight": 3}
            ]
        },
        {
            "question": "Self-Criticalness",
            "options": [
                {"option": "I don't criticize myself more than usual", "weight": 0},
                {"option": "I am more critical of myself than I used to be", "weight": 1},
                {"option": "I criticize myself for all of my faults", "weight": 2},
                {"option": "I blame myself for everything bad that happens", "weight": 3}
            ]
        },
        {
            "question": "Suicidal Thoughts or Wishes",
            "options": [
                {"option": "I don't have any thoughts of killing myself", "weight": 0},
                {"option": "I have thoughts of killing myself, but I would not carry them out", "weight": 1},
                {"option": "I would like to kill myself", "weight": 2},
                {"option": "I would kill myself if I had the chance", "weight": 3}
            ]
        },
        {
            "question": "Crying",
            "options": [
                {"option": "I don't cry anymore than usual", "weight": 0},
                {"option": "I cry more than I used to", "weight": 1},
                {"option": "I cry over every little thing", "weight": 2},
                {"option": "I feel like crying, but I can't", "weight": 3}
            ]
        },
        {
            "question": "Agitation",
            "options": [
                {"option": "I am no more restless or wound up than usual", "weight": 0},
                {"option": "I feel more restless or wound up than usual", "weight": 1},
                {"option": "I am so restless or agitated that it's hard to stay still", "weight": 2},
                {"option": "I am so restless or agitated that I have to keep moving or doing something", "weight": 3}
            ]
        },
        {
            "question": "Loss of Interest",
            "options": [
                {"option": "I have not lost interest in other people or activities", "weight": 0},
                {"option": "I am less interested in other people or things than before", "weight": 1},
                {"option": "I have lost most of my interest in other people or things", "weight": 2},
                {"option": "It's hard to get interested in anything", "weight": 3}
            ]
        },
        {
            "question": "Indecisiveness",
            "options": [
                {"option": "I make decisions about as well as ever", "weight": 0},
                {"option": "I find it more difficult to make decisions than usual", "weight": 1},
                {"option": "I have much greater difficulty in making decisions than I used to", "weight": 2},
                {"option": "I have trouble making any decisions", "weight": 3}
            ]
        },
        {
            "question": "Worthlessness",
            "options": [
                {"option": "I do not feel I am worthless", "weight": 0},
                {"option": "I don't consider myself as worthwhile or useful as I used to", "weight": 1},
                {"option": "I feel more worthless compared to others", "weight": 2},
                {"option": "I feel utterly worthless", "weight": 3}
            ]
        },
        {
            "question": "Loss of Energy",
            "options": [
                {"option": "I have as much energy as ever", "weight": 0},
                {"option": "I have less energy than I used to have", "weight": 1},
                {"option": "I don't have enough energy to do very much", "weight": 2},
                {"option": "I don't have enough energy to do anything", "weight": 3}
            ]
        },
        {
            "question": "Changes in Sleeping Patterns",
            "options": [
                {"option": "I have not experienced any change in my sleeping pattern", "weight": 0},
                {"option": "I sleep somewhat more than usual", "weight": 1},
                {"option": "I sleep somewhat less than usual", "weight": 1},
                {"option": "I sleep a lot more than usual", "weight": 2},
                {"option": "I sleep a lot less than usual", "weight": 2},
                {"option": "I sleep most of the day", "weight": 3},
                {"option": "I wake up one or two hours earlier and can't get back to sleep", "weight": 3}
            ]
        },
        {
            "question": "Irritability",
            "options": [
                {"option": "I am no more irritable than usual", "weight": 0},
                {"option": "I am more irritable than usual", "weight": 1},
                {"option": "I am much more irritable than usual", "weight": 2},
                {"option": "I am irritable all the time", "weight": 3}
            ]
        },
        {
            "question": "Changes in Appetite",
            "options": [
                {"option": "My appetite has not changed", "weight": 0},
                {"option": "I have a slightly reduced appetite", "weight": 1},
                {"option": "I have a slightly increased appetite", "weight": 1},
                {"option": "I have a much reduced appetite", "weight": 2},
                {"option": "I have a much increased appetite", "weight": 2},
                {"option": "I have no appetite at all", "weight": 3},
                {"option": "I constantly want to eat", "weight": 3}
            ]
        },
        {
            "question": "Difficulty Concentrating",
            "options": [
                {"option": "I can concentrate as well as ever", "weight": 0},
                {"option": "I can't concentrate as well as usual", "weight": 1},
                {"option": "It's hard to keep my mind on anything for very long", "weight": 2},
                {"option": "I find I can't concentrate on anything", "weight": 3}
            ]
        },
        {
            "question": "Tiredness or Fatigue",
            "options": [
                {"option": "I am no more tired or fatigued than usual", "weight": 0},
                {"option": "I get more tired or fatigued more easily than usual", "weight": 1},
                {"option": "I am too tired or fatigued to do a lot of the things I used to do", "weight": 2},
                {"option": "I am too tired or fatigued to do most of the things I used to do", "weight": 3}
            ]
        },
        {
            "question": "Loss of Interest in Sex",
            "options": [
                {"option": "I have not noticed any recent change in my interest in sex", "weight": 0},
                {"option": "I am less interested in sex than I used to be", "weight": 1},
                {"option": "I am much less interested in sex now", "weight": 2},
                {"option": "I have lost interest in sex completely", "weight": 3}
            ]
        }
    ]

    observations = []
    total_score = 0

    for q in questions:
        st.markdown('<div class="question-box"><br>', unsafe_allow_html=True)
        st.markdown(f'<div class="custom-text"><b>{q["question"]}</b></div>', unsafe_allow_html=True)
        selected_option = st.radio("Select an option:", [opt["option"] for opt in q["options"]], key=q["question"])
        for opt in q["options"]:
            if opt["option"] == selected_option:
                total_score += opt["weight"]
                observations.append(f"{q['question']}: {selected_option}")
        st.markdown('</br></div>', unsafe_allow_html=True)

    if st.button("Calculate Score"):
        st.write(f"Your total score is: {total_score}")

        if total_score < 14:
            st.write("You may have minimal depression.")
        elif 14 <= total_score < 20:
            st.write("You may have mild depression.")
        elif 20 <= total_score < 29:
            st.write("You may have moderate depression.")
        else:
            st.write("You may have severe depression.")

    # Generate summary when the button is clicked
    if st.button("Generate Summary"):
        summary = generate_summary("\n".join(observations), total_score)
        
        # Display summary in Streamlit
        
        st.write("### Summary of Patient's Mental Health")
        st.markdown(f'<div class="summary-box"><b>{summary}</b></div>', unsafe_allow_html=True)