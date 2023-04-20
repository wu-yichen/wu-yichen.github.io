import os
from flask import Flask, render_template, request, redirect, jsonify
import openai
from openai.error import RateLimitError

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def my_home():
    return render_template("index.html")


@app.route("/work1", methods=["GET", "POST"])
def gpt4():
    user_input = (
        request.args.get("user_input")
        if request.method == "GET"
        else request.form["user_input"]
    )
    messages = [{"role": "user", "content": user_input}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        content = response.choices[0].message["content"]
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."

    return jsonify(content=content)


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
