from langgraph.graph import StateGraph ,START ,END ,add_messages
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver

# loading api key
load_dotenv()

model  = ChatGroq(model_name = 'openai/gpt-oss-20b' , max_tokens=200)

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

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

# thread_id = '1'
# while True:
#     user_message =  input('Enter here: ')
#     print('User: ',user_message)

#     configure = {'configurable':{'thread_id':thread_id}}
#     if user_message.strip().lower() in ['quit','bye','end']:
#         break

#     response = workflow.invoke({'message':[user_message]},config=configure)
#     print(response['message'][-1].content)
