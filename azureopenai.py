


import os
# Import Azure OpenAI
import openai
from langchain_community.chat_models import AzureChatOpenAI

OPENAI_DEPLOYMENT_NAME = ""

os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = ""

llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
                           temperature=os.environ.get("TEMPERATURE", 0),
                           model=os.environ.get("MODEL", default="gpt-35-turbo"),
                           api_version=os.environ.get("API_VERSION", default="2023-08-01-preview"))

# print(llm.invoke("What is the Azure OpenAI Service?"))
