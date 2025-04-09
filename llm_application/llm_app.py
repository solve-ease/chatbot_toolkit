from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class llm:
    def __init__(self, model_name : str , model_provider : str):
        self.model = init_chat_model(
            model=model_name,
            model_provider=model_provider
        )

    def create_prompt_template(self , template: ChatPromptTemplate): # pass a prompt template to maintain while calling the llm
        self.prompt_template = template

    def stream(self, inp: tuple): # blocking streaming function to improve performance
        for i in self.model.stream(
            self.prompt_template.invoke(
                inp
            )
        ):
            yield i.content
    
    async def astream(self, inp: tuple): # non-blocking streaming function to improve performance
        for i in self.model.stream(
            self.prompt_template.invoke(
                inp
            )
        ):
            yield i.content
        
    def invoke(self, inp : tuple):
        return self.model.invoke(
            self.prompt_template.invoke(
                inp
            )
        ).content