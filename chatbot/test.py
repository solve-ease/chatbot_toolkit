from chatbot import chatbot
import asyncio

llm = chatbot(model_name = "deepseek/deepseek-chat-v3-0324:free" , model_provider = "openai")

llm.set_config({
    "configurable" : {"thread_id" : "1"}
})


llm.set_system_prompt("You are a helpful AI agent with the task of helping the user in any way possible")

while True:
    inp = input("User: ")
    print("AI: ",llm.invoke(inp) , flush=True)