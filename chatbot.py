import openai
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryBufferMemory, ConversationBufferMemory
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing 

in-depth explanations and discussions on a wide range of topics. As a language model, 

Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding 

conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and 

understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide 

range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, 

allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and 

information on a wide range of topics. Whether you need help with a specific question or just want to have a 

conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""
prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=6),
)


def stream2(input_text):
    return chatgpt_chain.predict(human_input=input_text)


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
