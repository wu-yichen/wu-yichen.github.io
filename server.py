import os
import openai
from flask import Flask, render_template, redirect, request, Response
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
persist_directory = "database/"
docsearch = Chroma(embedding_function=embeddings, persist_directory=persist_directory)


def gen_prompt(docs, query) -> str:
    return f"""To answer the question please only use the Context given, nothing else. Do not make up answer, simply say 'I don't know' if you are not sure.
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
            {"role": "user", "content": f"{input_text}"},
        ],
        stream=True,
        max_tokens=500,
        temperature=0,
    )
    for line in completion:
        if "content" in line["choices"][0]["delta"]:
            yield line["choices"][0]["delta"]["content"]


@app.route("/")
def my_home():
    return render_template("index.html")


@app.route("/work1", methods=["GET", "POST"])
def work1():
    if request.method == "POST":
        data = request.form
        input_text = data["user_input"]
        return Response(stream(input_text), mimetype="text/event-stream")

    return Response(None, mimetype="text/event-stream")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        return redirect("/thankyou.html")

    return "something went wrong"
