import streamlit as st
from chatbot_with_langGraph.backend.workflow import workflow
from langchain_core.messages import HumanMessage
import uuid


######################## Utility Functions ######################
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return workflow.get_state(config={'configurable':{'thread_id':thread_id}}
).values.get('message',[])

######################### INITIALIZE SESSION STATE ##############

# session dict from streamlit 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

######################### CONFIGURATION #########################


CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}

####################### DISPLAY PREVIOUS CHAT HISTORY #############

# loading the message history first
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

###################### GET USER INPUT #############################
user_input = st.chat_input('Type here')


############## PROCESS USER MESSAGE ###############################
if user_input:
    # add user message into history 
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

 # get ai message from backend
    # response = workflow.invoke({'message':[HumanMessage(content =user_input)]},config=CONFIG)
    # ai_message = response['message'][-1].content

####################  STREAM AI RESPONSE ###########################
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
   
################# Save AI response to chat history ##########################
 # add assistent message into history 
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    # with st.chat_message('assistant'):
    #     st.text(ai_message)

################################   Side Bar UI  #############################

st.sidebar.title('AI ChatBot')

if st.sidebar.button('New Chat'):
    reset_chat()
    st.rerun()


st.sidebar.header('Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role="user"
            else:
                role="assistant"
            temp_messages.append({'role':role,'content':msg.content})

        st.session_state['message_history'] = temp_messages