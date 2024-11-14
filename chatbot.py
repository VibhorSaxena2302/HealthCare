import streamlit as st
from llm_model import llm
import chroma

chatbot = llm()
chromadb_path = r'C:\Users\shrey\Git Uploads\HealthCare\LLM\db'

def chatbot_page():
    st.subheader("Chat with our HealthCare Assistant")

    # Persisting the chat history in the session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize the user input in session state if not present
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''

    # Custom CSS for aligning messages and making chat container scrollable
    chat_style = """
    <style>
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #000000;
        border-radius: 5px;
    }
    .user-message {
        text-align: right;
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        width: 60%;
        float: right;
        clear: both;
        color: black;
    }
    .assistant-message {
        text-align: left;
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        width: 60%;
        float: left;
        clear: both;
        color: black;
    }
    </style>
    """
    st.markdown(chat_style, unsafe_allow_html=True)

    # Placeholder for the chat messages
    chat_placeholder = st.empty()

    # Function to display chat messages
    def display_chat_messages(assistant_response=""):
        chat_html = '<div class="chat-container">'
        for message in st.session_state.messages:
            if message["role"] == "user":
                chat_html += f"<div class='user-message'>{message['content']}</div>"
            elif message["role"] == "assistant":
                chat_html += f"<div class='assistant-message'>{message['content']}</div>"
        # If there is an assistant_response being built, add it
        if assistant_response:
            chat_html += f"<div class='assistant-message'>{assistant_response}</div>"
        chat_html += '</div>'
        # Add JavaScript to scroll to the bottom
        chat_html += """
        <script>
        var chatContainer = document.querySelector('.chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        </script>
        """
        chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

    # Display chat messages at the start
    display_chat_messages()

    # Chat form
    with st.form(key='chat_form'):
        user_input = st.text_input("You: ", "")
        submit_button = st.form_submit_button(label="Send")

    # Process the input when the user submits a message
    if submit_button and user_input:
        # Add user's message to session state (to store chat history)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Initialize assistant's response
        assistant_response = ""

        # Display chat messages including the new user message
        display_chat_messages()

        db = chroma.get_chroma(chromadb_path)
        results = db.similarity_search_with_score(user_input, k=2)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results]).replace('\n', ' ')

        prompt = f'Answer the following query. Do not exceed 150 words:\n\n Query: {user_input}'

        if context_text != '':
            prompt += f'### CONTEXT ### \n\n {context_text}\n\n'

        # Get chatbot's streaming response using the llm instance
        for chunk in chatbot.stream_generate(prompt=user_input):
            # Update the assistant's response incrementally
            assistant_response += chunk
            # Display chat messages including the current assistant's response
            display_chat_messages(assistant_response)

        # After streaming ends, add the full response to session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Display chat messages including the full assistant's response
        display_chat_messages()