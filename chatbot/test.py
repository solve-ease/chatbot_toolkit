from chatbot import ChatBot
import asyncio

llm = ChatBot(model_name = "deepseek/deepseek-chat-v3-0324:free" , model_provider = "openai")

llm.set_config({
    "configurable" : {"thread_id" : "1"}
})

llm.set_system_prompt(f"i am providing you a html code, it is a template for a development road map  ypu just have to add content to that html file according to the project the user askes you to generate a roadmap of: ") 
# pro tip in the system prompt add that dont ever show that the word limit is of 100 words or add that you have to give concise answers to limit the token usage 

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