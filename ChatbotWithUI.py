from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from fastapi import FastAPI
from langserve import add_routes

load_dotenv()

model = ChatOpenAI()

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

app = FastAPI(
    title="Translate App",
    version="1.0.0",
    description="Translate into all languages",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model
config = {"configurable": {"session_id": "firstChat"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)

add_routes(app,chain,path="/chain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)


