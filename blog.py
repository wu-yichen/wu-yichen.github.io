import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_blog_topics(prompt1):
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=f"Generate blog topics on: {prompt1}.",
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response["choices"][0]["text"]


def generate_blog_sections(prompt1):
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=f"Expand the blog title in to high level blog sections: {prompt1} \n\n- Introduction: ",
        temperature=0.6,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response["choices"][0]["text"]


def blog_section_expander(prompt1):
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=f"Expand the in to a detailed professional , witty and clever explanation.\n\n {prompt1}",
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response["choices"][0]["text"]
