from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate 
from langchain_core.messages import SystemMessage

load_dotenv()

class state(TypedDict):
    messages: Annotated[list , add_messages]

class chatbot():
    def __init__(self, model_name , model_provider):
        self.model = init_chat_model(model=model_name , model_provider=model_provider)
        
        self.graphBuilder = StateGraph(state)

        self.graphBuilder.add_node("llm" , self.llm)
        self.graphBuilder.add_edge(START , "llm")
        self.graphBuilder.add_edge("llm" , END)

        checkpointer = MemorySaver()
        self.graph = self.graphBuilder.compile(checkpointer=checkpointer)

    def llm(self , state : state):
        return {
            "messages" : self.model.invoke(
                state["messages"]
            )
        }
    
    def set_config(self , config):
        # sample template : config = {"configurable" : {"thread_id" : n}}
        self.config = config
    
    def astream(self, message):
        pass

    def set_system_prompt(self, prompt):
        self.system_prompt = {"role":"system" , 'content' : prompt}
        self.graph.invoke({"messages" : self.system_prompt} , config=self.config)

    def invoke(self , message) : 
        return self.graph.invoke(
            {
                "messages" : message
            },config = self.config
        )["messages"][-1].content