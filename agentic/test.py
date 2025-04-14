from agentic_chatbot import agentic_chatbot
from langchain_community.tools.tavily_search import TavilySearchResults
import asyncio

tool = TavilySearchResults(max_results=2)

llm = agentic_chatbot(model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" , model_provider = "together", tools_list=[tool])

llm.set_config({
    "configurable" : {"thread_id" : "1"}
})


llm.set_system_prompt("You are a helpfull ai agent") # pro tip in the system prompt add that dont ever show that the word limit is of 100 words or add that you have to give concise answers to limit the token usage 

# async def temp():
while True:
    inp = input("User: ")
    if inp == 'q':
        break
    
    print("AI: ",end="")

    # async for i in llm.astream(inp):
    #     print(i,flush=True , end="")

    print(llm.invoke(inp) , flush=True)
    print()

      
# asyncio.run(temp())