import streamlit as st
import openai

# App title
st.set_page_config(page_title="🤗💬 Mental Health Support Assistant For GUU Scholars")

# OpenAI API Key
with st.sidebar:
    st.title('🤗💬 Mental Health Support Assistant For GUU Scholars')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('OpenAI API key provided!', icon='✅')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter OpenAI API Key:', type='password')
        if not openai_api_key:
            st.warning('Please enter your API key!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    # st.markdown('📖 Student Mental Health Support System [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')
    
    #markdown text
    st.markdown('📖 This app offers mental health support, resources, and advice to students, especially during stressful periods like exams.')
    
# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response using OpenAI API endpoint
def generate_response(prompt_input, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-0125",
        prompt=prompt_input,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, openai_api_key) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
