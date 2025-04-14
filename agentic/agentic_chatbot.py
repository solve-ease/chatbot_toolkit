from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import ToolMessage
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately

load_dotenv()

class State (TypedDict):
    messages : Annotated[list, add_messages]

class agentic_chatbot():
    def __init__(self , model_name , model_provider , tools_list):

        self.model = init_chat_model(model=model_name, model_provider=model_provider)
        
        self.tools = {tool.name : tool for tool in tools_list}

        self.model = self.model.bind_tools(tools_list)

        self.grpahBuilder = StateGraph(State)
        
        self.grpahBuilder.add_node("llm" , self.__llm)
        self.grpahBuilder.add_node("tools" , self.__call_tool)

        self.grpahBuilder.add_edge(START , "llm")
        self.grpahBuilder.add_conditional_edges("llm" , self.__route_tool , {"END" : END , "tools" : "tools"})
        self.grpahBuilder.add_edge("tools" , "llm")

        checkpointer = MemorySaver()
        self.graph = self.grpahBuilder.compile(checkpointer=checkpointer)
    
    def __llm(self , state: State):
        return {"mesages" : [{
            "role" : "ai",
            "content" : self.model.invoke(state["messages"])
        }]}
    
    def __call_tool(self , message: State):
        tool_calls = message["messages"][-1]["tool_calls"]
        
        output = []
        for tool_call in tool_calls:
            tool_output = self.tools.get(tool_call["name"]).invoke(
                tool_call["args"]
            )

            output.append(ToolMessage(
                content=tool_output,
                tool_name = tool_call["name"],
                tool_id = tool_call["id"]
            ))

        return {"messages" : output}
    
    def __route_tool(self , message: State):

        ai_message = message["messages"][-1]

        if hasattr(ai_message , "tool_calls") and len(ai_message["tool_calls"]) > 0:
            return "tools"
        
        return "END"
    
    def set_config(self , config):
        # sample template : config = {"configurable" : {"thread_id" : n}}
        self.config = config
        self.thread_key = config["configurable"]["thread_id"]
    
    async def astream(self, message):

        # print(self.graph.get_state(self.config))

        response = ""

        all_msgs = self.graph.get_state(self.config).values["messages"] + [{"role":  "user" , "content": message}]
        self.graph.update_state(self.config , {"messages": all_msgs})

        async for chunk in self.model.astream(
            trim_messages(
                all_msgs,
                max_tokens = 10000,
                token_counter = count_tokens_approximately,
                include_system = True,
                allow_partial = True 
            )
        ):
            # print(chunk)
            response += chunk.content
            yield chunk.content
        
        ai_message = [{"role" : "ai" , "content" : response}]
        all_msgs = self.graph.get_state(self.config).values["messages"] + ai_message

        # print(all_msgs)
        self.graph.update_state(self.config , {"messages": all_msgs})

    def set_system_prompt(self, prompt):
        self.system_prompt = [{"role":"system" , 'content' : prompt}]
        self.graph.update_state(self.config , {"messages": self.system_prompt})

    def invoke(self , message) :
        temp = self.graph.invoke(
            {
                "messages" : message
            },config = self.config
        )
        
        return temp["messages"][-1].content