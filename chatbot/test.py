from chatbot import chatbot
import asyncio

llm = chatbot(model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" , model_provider = "together")

llm.set_config({
    "configurable" : {"thread_id" : "1"}
})


llm.set_system_prompt("You are a helpful AI agent with the task of helping the user in any way possible")

async def temp():
    while True:
        inp = input("User: ")
        if inp == 'q':
            break
        
        print("AI: ",end="")

        async for i in llm.astream(inp):
            print(i,flush=True , end="")
        print()
        
asyncio.run(temp())