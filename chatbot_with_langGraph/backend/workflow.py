from langgraph.graph import StateGraph ,START ,END ,add_messages
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# loading api key
load_dotenv()

model  = ChatGroq(model_name = 'openai/gpt-oss-20b' , max_tokens=900 , reasoning_effort='low')

#state
class chat_state(TypedDict):
    message:Annotated[list[BaseMessage], add_messages]


# task
def chat_node(state:chat_state)->chat_state:
    sms = state['message']
    response = model.invoke(sms)
    return { 'message':[response]}

# define graph
graph = StateGraph(chat_state)

# nodes
graph.add_node('chat_node',chat_node)

# edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


connection = sqlite3.connect(database='chatbot.db',check_same_thread=False)

# checkpointer
checkpointer = SqliteSaver(conn=connection)

workflow = graph.compile(checkpointer=checkpointer)


# we need thread ids to pass in config from the database so we can access the store chats 
def threads_retriever():
    all_threads = set()
    for checkpoit in checkpointer.list(None):
        all_threads.add(checkpoit.config['configurable']['thread_id'])
    return list(all_threads)

# testing_list = threads_retriever()
# print(testing_list)
# thread_id = '1'
# while True:
#     user_message =  input('Enter here: ')
#     print('User: ',user_message)

# configure = {'configurable':{'thread_id':thread_id}}
#     if user_message.strip().lower() in ['quit','bye','end']:
#         break

#     response = workflow.invoke({'message':[user_message]},config=configure)
#     print(response['message'][-1].content)


# implement streaming on the ai response

# for chunck,metadata in workflow.stream(
#     {'message':['write an essay on gpu with 650 words']},
#     config=configure,
#     stream_mode='messages'
# ):
#     if chunck.content:
#         print(chunck.content , end='',flush=True)