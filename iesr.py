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

    scores = []
    observations = []  # List to collect observations for summary

    for i, q in enumerate(questions):
        selected = st.radio(q["question"], [opt["option"] for opt in q["options"]], key=f"q{i}")
        score = next(opt["weight"] for opt in q["options"] if opt["option"] == selected)
        scores.append(score)
        observations.append(f"{q['question']}: {selected}")  # Collect observations4

    total_score = sum(scores)

    if st.button("Calculate IES-R Score"):
        
        st.write(f"Your total score is: {total_score}")

        # Display symptom severity based on the score
        if total_score < 24:
            st.write("You may have minimal emotional distress.")
        elif 24 <= total_score < 33:
            st.write("You may have mild distress.")
        elif 33 <= total_score < 36:
            st.write("You may have moderate distress. (likely PTSD symptons)")
        else:
            st.write("You may have severe emotional distress, indicating a strong liklihood of PTSD.")

        # Generate summary when the button is clicked
    if st.button("Generate Summary"):
        summary = generate_summary("\n".join(observations), total_score)
            
        # Display summary in Streamlit
        st.write("### Summary of Patient's Mental Health")
        st.write(summary)