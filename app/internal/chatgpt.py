from openai import OpenAI
import openai
import os


#print(f"Using OpenAI API key: {api_key}")
# os.environ["OPENAI_API_KEY"] = api_key
gpt_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ASSISTANT_ID = os.environ["OPENAI_ASSISTANT_ID"]


# thread = client.beta.threads.create()
# print(f"Thread created with ID: {thread.id}")
