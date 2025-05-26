import json
import os
import re

from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def review_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    with open("prompt.txt", "r") as f:
        prompt = f.read()

    prompt = PromptTemplate(input_variables=["text"], template=prompt)

    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")

    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    result = chain.run(documents)
    # print("\n======= Resume Review =======")
    print(result)
    if "```json\n" in result:
        match = re.search("```json\n*(.*)\n*```", result, re.DOTALL)
        if match:
            json_result = match.group(1)
            result = json.loads(json_result)
    else:
        result = json.loads(result)
    return result

# r = review_resume(r"C:\Users\ASUS\OneDrive\Documents\resume\Arnab_Sen_Resume.pdf")
# print(r)
# print(type(r))