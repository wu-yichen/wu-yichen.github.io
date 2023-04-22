import os
import openai

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


openai.api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
docsearch = Chroma(embedding_function=embeddings, persist_directory="database/")


def gen_prompt(docs, query) -> str:
    return f""" To answer the question please only use the Context given, nothing else.
                Do not make up answer, simply say 'I don't know' if you are not sure.
                Question: {query}
                Context: {[doc.page_content for doc in docs]}
                Answer:
            """


def prompt(query):
    docs = docsearch.similarity_search(query, k=4)
    return gen_prompt(docs, query)


def stream(input_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an assistant."},
            {"role": "user", "content": f"{prompt(input_text)}"},
        ],
        stream=True,
        max_tokens=500,
        temperature=0,
    )
    for line in completion:
        if "content" in line["choices"][0]["delta"]:
            yield line["choices"][0]["delta"]["content"]
