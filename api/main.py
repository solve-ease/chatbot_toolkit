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

        llm.set_system_prompt("You are a helpful AI agent with the task of helping the user in any way possible. Dont give any answer larger than 100 words, but also dont make them too short either")

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

