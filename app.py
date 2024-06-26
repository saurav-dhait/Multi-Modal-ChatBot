import streamlit as st
from llm import (generate_choice_chain,
                 generate_img_to_text_chain,
                 generate_text_to_code_chain,
                 generate_text_to_text_chain,
                 generate_text_to_img_chain,
                 generate_image_url,
                 convert_to_base64)
from PIL import Image


def main():
    # variables
    response = "No response"
    flag = 0
    if "choice_chain" not in st.session_state:
        st.session_state["choice_chain"] = generate_choice_chain()
    if "text_to_text_chain" not in st.session_state:
        st.session_state["text_to_text_chain"] = generate_text_to_text_chain()
    if "img_to_text_chain" not in st.session_state:
        st.session_state["img_to_text_chain"] = generate_img_to_text_chain()
    if "text_to_img_chain" not in st.session_state:
        st.session_state["text_to_img_chain"] = generate_text_to_img_chain()
    # page config
    st.set_page_config(page_title="Multi-LLM chatbot",
                       page_icon="💬",
                       layout="centered",
                       initial_sidebar_state="expanded",
                       menu_items=None)

    # sidebar
    with st.sidebar:
        st.subheader("Chat options")
        clear_chat = st.button("Clear chat", type="primary")

        image_file = st.file_uploader("Upload image")

    # main body
    st.title("💬 Multi-Modal Chatbot : ")
    # message handling
    if clear_chat:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hey, how can i help you ? "}]
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hey, how can i help you ? "}]
    for msg in st.session_state.messages:
        if isinstance(msg["content"], str):
            st.chat_message(msg["role"]).write(msg["content"])
        else:
            st.chat_message(msg["role"]).image(msg["content"])
    # user query handling
    if query := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").write(query)
        with st.spinner("Choosing the appropriate LLM"):
            llm_choice = st.session_state.choice_chain.invoke({"query": query})
        llm = ""
        try:
            llm_choice = int(llm_choice)
        except ValueError:
            llm_choice = 1

        with st.spinner(f"Generating response"):
            match llm_choice:
                case 1:
                    llm = "llama3"
                    response = st.session_state.text_to_text_chain.invoke({"query": query})
                case 2:
                    llm = "llava"
                    if image_file is None:
                        response = "please upload an image"
                    else:
                        pil_image = Image.open(image_file)
                        image_b64 = convert_to_base64(pil_image)
                        st.session_state.messages.append({"role": "user", "content": image_file})
                        st.chat_message("user").image(image_file)
                        response = st.session_state.img_to_text_chain.invoke({"text": query, "image": image_b64})
                case 3:
                    llm = "DALL-e"
                    response = "The image is located at the below URL : " + generate_image_url(
                        st.session_state.text_to_img_chain, query)

            st.session_state.messages.append({"role": "assistant", "content": f"{llm} Response :\n\n" + response})
            st.chat_message("assistant").write(f"{llm} Response :\n\n" + response)


if __name__ == '__main__':
    main()
