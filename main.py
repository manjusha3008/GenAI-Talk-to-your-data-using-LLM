import PyPDF2
import requests
import io
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
import pprint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI
import os
from azureopenai import OPENAI_DEPLOYMENT_NAME

def concatenate_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://xit-openai-exploration-projects.openai.azure.com/"
# os.environ["AZURE_OPENAI_API_KEY"] = "fe33c38349284de390fdf816a99976cc"
# OPENAI_DEPLOYMENT_NAME = "gpt-35-turbo-chatxipt-analysis"
# URL of the PDF file
url = "https://www.bitkom.org/sites/main/files/2024-02/bitkom-studie-klimaeffekte-der-digitalisierung-2.pdf"

# Send a GET request to the URL
response = requests.get(url)
chapter_list = ["2", "4", "12", "20", "84", "89", "92", "94"]
# Check if the request was successful
if response.status_code == 200:
  with open("extracted_text.txt", "w", encoding='utf-8') as text_file:
    # Read the content of the response
      pdf_content = response.content

      # Create a file-like object from the PDF content
      pdf_file = io.BytesIO(pdf_content)

      # Create a PDF reader object
      pdf_reader = PyPDF2.PdfReader(pdf_file)

      # Initialize an empty string to store the extracted text
      text = ""
      text1 = ""

      # Iterate through each page of the PDF
      for page_num in range(4,12):
          # Extract text from the current page
          text = pdf_reader.pages[page_num].extract_text()
          text = '\n'.join(text.split('\n'))
          text1 += text 
          text_file.write(text)


      llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
                           temperature=os.environ.get("TEMPERATURE", 0),
                           model=os.environ.get("MODEL", default="gpt-35-turbo"),
                           api_version=os.environ.get("API_VERSION", default="2023-08-01-preview"))
      answer = llm.invoke( text1 +" Summarize the text in german").to_json()

      # Show the LLMs detailed output.
  
      print(answer["kwargs"]["content"])

else:
    # Print an error message if the request was not successful
    print("Failed to retrieve PDF file")



