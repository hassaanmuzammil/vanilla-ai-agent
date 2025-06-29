import chainlit as cl
import chainlit.data as cl_data
from chainlit.data.sqlalchemy import SQLAlchemyDataLayer

from src.agent import Agent
from src.config import SYSTEM_PROMPT_TEMPLATE, KNOWN_ACTIONS, DB_SCHEMA
from src.config import (
    CHAINLIT_DB_NAME,
    CHAINLIT_DB_USER,
    CHAINLIT_DB_PASSWORD,
    CHAINLIT_DB_HOST,
    CHAINLIT_DB_PORT
)
from src.llm import llm

conn_info = f"postgresql+asyncpg://{CHAINLIT_DB_USER}:{CHAINLIT_DB_PASSWORD}@{CHAINLIT_DB_HOST}:{CHAINLIT_DB_PORT}/{CHAINLIT_DB_NAME}"
cl_data.data_layer = SQLAlchemyDataLayer(conn_info, ssl_require=False)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("llm", llm)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=DB_SCHEMA)
    cl.user_session.set("system_prompt", system_prompt)
    cl.user_session.set("known_actions", KNOWN_ACTIONS)
    

@cl.password_auth_callback
async def password_auth_callback(username: str, password: str):
    # Dummy auth logic
    if username == "admin" and password == "password":
        return cl.User(
            id="admin",
            name="Administrator"
        )
    return False

@cl.on_message
async def on_message(message: cl.Message):
    
    try:      
        llm = cl.user_session.get("llm")
        system_prompt = cl.user_session.get("system_prompt")
        known_actions = cl.user_session.get("known_actions")

        # for now initialize agent here, later shift to on_chat_start
        agent = Agent(
            llm=llm,
            system_prompt=system_prompt,
            known_actions=known_actions,
            react_json=True,
            max_iterations=10,
            stop_words=("PAUSE",)
        )

        async with cl.Step(name="Intermediate Steps") as step: 
            res = ""
            async for chunk in agent.run(message.content):
                res += chunk
                await step.stream_token(chunk)
            # step.output = res

        await cl.Message(content="Workflow completed successfully.").send()

    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send()
    
    return

@cl.on_chat_end
def end():
    pass

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)

    # CMD > chainlit run main.py --host 0.0.0.0 --port 8000 -h