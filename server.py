import os
import openai
import chatbot
from flask import Flask, render_template, redirect, request, Response


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def my_home():
    return render_template("index.html")


@app.route("/work1", methods=["GET", "POST"])
def work1():
    if request.method == "POST":
        data = request.form
        input_text = data["user_input"]
        return Response(chatbot.stream(input_text), mimetype="text/event-stream")

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
