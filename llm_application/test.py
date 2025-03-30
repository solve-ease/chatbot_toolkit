from llm_application.llm_app import llm
from langchain_core.prompts import ChatPromptTemplate


model = llm("deepseek/deepseek-chat-v3-0324:free" , "openai")

model.create_prompt_template(
    ChatPromptTemplate.from_messages(
        [
            ("system" , "you are a helpful ai assitanct whose work it answer all the questions and correct any grammatical error in the question given"),

            ("user" , "{text}")
        ]
    )
)

for i in model.stream(("what should we do today")):
    print(i,end="")

print("\n")