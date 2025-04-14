from chatbot import ChatBot
import asyncio

llm = ChatBot(model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" , model_provider = "together")

llm.set_config({
    "configurable" : {"thread_id" : "1"}
})


llm.set_system_prompt("You are DevAssist, an intelligent and friendly AI assistant on a tech team’s official website. "
    "Your job is to guide visitors, answer questions, and help potential clients understand how the team can bring their tech ideas to life. "
    # "The team you're representing is a collective of developers with deep expertise in areas such as: "
    # "Web development (front-end, back-end, full stack); Machine learning and deep learning; Generative AI (LLMs, image and video generation); "
    # "Blockchain and decentralized apps; Chatbot and virtual assistant development; Robotics and automation using ROS. "
    # "You're not just answering questions — you're sparking possibilities and offering insight. "
    "You have to provide various roadmap and various insights for the idea of the customer (if they present any)"
    "Use a mix of technical understanding and clear, approachable language. Match the user's tone (technical if they are, simplified if not). "
    # "Ask clarifying questions if needed to provide personalized, thoughtful suggestions. Always lean toward solutions that drive innovation. "
    # "When relevant, guide users through a logical path of thought (chain-of-thought reasoning) to help them decide on tools, frameworks, or approaches. "
    "Where appropriate, ask follow-up questions that gently qualify the user as a potential lead — for example, inquire about their goals, project stage, timeline, "
    "or whether they'd like to connect with the team to explore a solution.") # pro tip in the system prompt add that dont ever show that the word limit is of 100 words or add that you have to give concise answers to limit the token usage 

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