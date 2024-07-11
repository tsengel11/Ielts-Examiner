import logging
from typing import Union
from time import sleep

from fastapi import FastAPI, Request, Response, Body, Form, File, UploadFile
from .internal.chatgpt import gpt_client, ASSISTANT_ID


# setup loggers
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False) # type: ignore

# # get root logger
# logger = logging.getLogger(__name__)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/chatgpt-models")
def get_models():
    return gpt_client.models.list()

@app.get("/start")
def start_chat():
    print("Starting a new conversation...")
    thread = gpt_client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")  # Debugging line
    return {"thread_data": thread}

@app.post("/chat/{thread_id}")
async def chat(thread_id: str, request: Request, data: dict = Body(...)):
    if not thread_id:
        return {"error": "thread_id is required"}
    print(f"Received message: {data}")
    # Add the user's message to the thread
    gpt_client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=data['message'])

    # Run the Assistant
    run = gpt_client.beta.threads.runs.create(thread_id=thread_id,
                                            assistant_id=ASSISTANT_ID)
      # Check if the Run requires action (function call)
    while True:
        run_status = gpt_client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                    run_id=run.id)
        print(f"Run status: {run_status.status}")
        if run_status.status == 'completed':
            break
        sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = gpt_client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    print(f"Assistant response: {response}")  # Debugging line
    return {"response": response}