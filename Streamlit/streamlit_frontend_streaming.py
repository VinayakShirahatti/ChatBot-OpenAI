"""
The major problem what our simple chatbot faced was : whenever we asked for a big response it used to generate the response in the backend and then 
provide the entire response in the UI at once , which made user wait for long time until the response is generated in the bakend ..
To solve this problem we will be using Streaming which is basically it prints the response character by character like how ChatGPT uses ..

Streaming : Streaming means the LLM sends the output piece by piece (token by token) while it is still generating, instead of waiting to finish 
the whole answer.

So you see the text appearing live, just like typing.

✅ Why Streaming is Useful?
Faster response
You don’t wait for the full answer. Output starts immediately.

Better UI/UX
Looks natural—like the model is typing in real time.

Improves performance for long answers
Long responses don’t block the system; users can read while generation continues.

Good for chatbots, streaming apps, dashboards.

Streaming is important for Multi-Modal UIs such as Alexa etc

We will be using Generator to implement Streaming :
Generator : A generator is a special function in Python that gives you one value at a time, instead of giving everything at once.
It does this using yield instead of return . 

Generator does NOT store all values.
It produces the next value only when needed.
Saves memory.
Starts where it left off.

FULL SIMPLE FLOW:
User sends input
LLM starts streaming output chunks
write_stream() prints chunks LIVE
The combined final message is saved to history
Next time the page reruns, the assistant bubble still shows the message

"""

import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

#=============================================SESSION STATE =============================================#
# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

#==============================================MAIN UI ====================================================#
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):
                                                                                        #st.write_stream(...):This tells Streamlit to display each chunk LIVE as it is received
        ai_message = st.write_stream(                                                   #message_chunk.content for message_chunk, metadata in : This is a generator expression.
            message_chunk.content for message_chunk, metadata in chatbot.stream(        #Chatbot.stream:This calls the LLM in streaming mode.It returns a generator that yields:
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
