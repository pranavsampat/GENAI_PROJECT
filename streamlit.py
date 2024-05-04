import streamlit as st
from working_code import recognize_speech, translate_text, execute_intent

# App title
st.set_page_config(page_title="Your AI Assistant")

# Sidebar
with st.sidebar:
    st.title("Gen Ai Project")
    st.write("Name: Pranav Sampat <br> USN: 1RVU22BSC071",unsafe_allow_html=True)

# Centered chat box
chat_container = st.container()

# Initialize empty list to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
with chat_container:
    st.write("## Chat with Your AI Assistant")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function for generating AI assistant response
def generate_response(prompt_input):
    translated_text = translate_text(prompt_input, 'auto', 'en') 
    response = execute_intent(translated_text.lower(), 'en')
    return response

# Record and recognize user voice input
if st.button("Speak"):
    user_input = recognize_speech()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
            st.write('Response:',response)

# Text input for users who prefer typing
user_input_text = st.text_input("Enter your message:")
if st.button("Send"):
    if user_input_text:
        st.session_state.messages.append({"role": "user", "content": user_input_text})
        with st.spinner("Thinking..."):
            response = generate_response(user_input_text)
            st.write('Respone:',response)