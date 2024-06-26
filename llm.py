from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import base64
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def generate_choice_chain():
    llm = ChatOllama(model="llama3")
    system_prompt = ("""
    You are a helpful assistant. The human will ask a question, and you have to answer it. 
    However, there are some rules and regulations you must follow while giving your answer. 
    The rules are as follows:
    1. Respond with only one integer.
    2. Strictly respond with integers.
    3. You have to choose between three integers: 1, 2 and 3.
    4. If asked to describe an image or photo, respond with 2.
    5. If asked to make, create, draw, or generate an image/photo, respond with 3.
    6. For all other questions, respond with 1.
    7. Your response should be a single integer without any additional text.
    """)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{query}")
        ]
    )
    chain = prompt | llm | StrOutputParser()
    return chain


def generate_text_to_text_chain():
    llm = ChatOllama(model="llama3")
    system_prompt = ("You are a helpful assistant"
                     "please answer the question strictly in 3 to 5 lines."
                     )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{query}")
        ]
    )
    chain = prompt | llm | StrOutputParser()

    return chain


def generate_text_to_code_chain():
    llm = ChatOllama(model="codellama")
    system_prompt = ("You are a helpful assistant"
                     "please answer the question strictly in 3 to 5 lines."
                     )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{query}")
        ]
    )
    chain = prompt | llm | StrOutputParser()

    return chain


def generate_img_to_text_chain():
    llm = ChatOllama(model="llava")
    chain = prompt_func | llm | StrOutputParser()
    return chain


def generate_text_to_img_chain():
    llm = OpenAI()
    system_prompt = ("You are a helpful assistant"
                     "Generate a detailed prompt under 30 words to generate an image based on the "
                     "description provided by the human"
                     )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{query}")
        ]
    )
    chain = prompt | llm
    return chain


def generate_image_url(chain, query):
    image_url = DallEAPIWrapper().run(chain.invoke({"query": query}))
    return image_url


def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def prompt_func(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]
