import streamlit as st
from chatbot_with_langGraph.backend.workflow import workflow
from langchain_core.messages import HumanMessage

thread_id = '1'
CONFIG = {'configurable':{'thread_id':thread_id}}

# session dict from streamlit 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# message_history = []

# loading the message history first
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here')



if user_input:
    # add user message into history 
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

 # get ai message from backend
    # response = workflow.invoke({'message':[HumanMessage(content =user_input)]},config=CONFIG)
    # ai_message = response['message'][-1].content

    ai_message = st.write_stream(
        message_chunk.content for message_chunk ,meta_data in workflow.stream(
                {'message':[user_input]},
                 config=CONFIG,
                 stream_mode='messages'
        ) 
    )

    # workflow.stream({'message':[HumanMessage(content =user_input)]},
    #                            config=CONFIG,
    #                            stream_mode='messages'
    #                            )
   

 # add assistent message into history 
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    
    # with st.chat_message('assistant'):
    #     st.text(ai_message)