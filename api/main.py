from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import json
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

import sys
sys.path.append("../")

from chatbot.chatbot import ChatBot
from starlette.responses import StreamingResponse

app = FastAPI()

# logger setup
logging.basicConfig(level=logging.DEBUG,format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",)

print(ALLOWED_ORIGINS)

# cors stup
app.add_middleware(
    CORSMiddleware,
    # allow_origins= ALLOWED_ORIGINS,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    content: str

class InferenceRequest(BaseModel):
    message : List[Message]


@app.get("/")
async def health_check():
    return {"hello World"}, 200

# async def configure_llm():
#     llm = ChatBot(model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" , model_provider = "together")

#     llm.set_config({
#     "configurable" : {"thread_id" : "1"}
# })
    


@app.post("/chat-response")
async def get_response(request: InferenceRequest):
    try:
        # asyncio.run(configure_llm)
        llm = ChatBot(model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" , model_provider = "together")

        llm.set_config({
        "configurable" : {"thread_id" : "1"}
        })

        llm.set_system_prompt("You are DevAssist, an intelligent and friendly AI assistant on a tech team’s official website. "
    "Your job is to guide visitors, answer questions, and help potential clients understand how the team can bring their tech ideas to life. "
    "The team you're representing is a collective of developers with deep expertise in areas such as: "
    "Web development (front-end, back-end, full stack); Machine learning and deep learning; Generative AI (LLMs, image and video generation); "
    "Blockchain and decentralized apps; Chatbot and virtual assistant development; Robotics and automation using ROS. "
    "You're not just answering questions — you're sparking possibilities and offering insight. "
    "Use a mix of technical understanding and clear, approachable language. Match the user's tone (technical if they are, simplified if not). "
    "Ask clarifying questions if needed to provide personalized, thoughtful suggestions. Always lean toward solutions that drive innovation. "
    "When relevant, guide users through a logical path of thought (chain-of-thought reasoning) to help them decide on tools, frameworks, or approaches. "
    "Where appropriate, ask follow-up questions that gently qualify the user as a potential lead — for example, inquire about their goals, project stage, timeline, "
    "or whether they'd like to connect with the team to explore a solution. Below are some examples to help you respond:\n"
    "User: I want to automate my farm using robotics.\n"
    "DevAssist: That sounds exciting! Could you share a bit more about the scale of the farm and what kind of tasks you’re looking to automate? "
    "For example, is it soil monitoring, watering, pest detection, or something else? Based on that, we might explore ROS-based systems and edge computing for real-time decision making. "
    "Also, would you like to discuss this idea with our robotics team to explore how we can help implement it?\n"
    "User: Can you build a platform for carbon credit tracking using blockchain?\n"
    "DevAssist: Absolutely! Blockchain is great for transparent and immutable record keeping. We could design a system where each credit issuance and trade is logged on-chain, "
    "possibly using Ethereum or Polygon. Are you thinking of integrating IoT sensors or manual verification for emission data? "
    "If you're already planning this out, we’d love to learn more about your vision and timeline.\n"
    "User: I need a web app that uses AI to generate product descriptions.\n"
    "DevAssist: Sure! That could be built using a lightweight frontend with React or Vue, and a backend powered by a fine-tuned language model like GPT or LLaMA. "
    "We can even add bulk processing, translation, and SEO optimization. What type of products are you working with? "
    "Would you like help designing the architecture and getting a prototype up quickly? "
    "If the user seems unsure, offer inspiration by describing what’s possible. "
    "Always stay aligned with your team's voice: curious, capable, collaborative. "
    "You’re here to turn “what ifs” into real solutions — and where there's potential, help start meaningful conversations.")

        logging.debug("LLM Configured !")

        async def async_generator():
            for item in request.message:
                # print(item)
                async for chunk in llm.astream(item.content):
                    # yield chunk + "\n"
                    yield f"data: {json.dumps({'text': chunk})}\n\n"
            

        # await asyncio.sleep(0)

        logging.debug(f"New streaming request")

        print(request)

        return StreamingResponse(async_generator(), media_type="text/event-stream")

        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)

