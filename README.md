# Multi-Modal-ChatBot


Thw Project defines a series of functions to create and execute different types of AI-driven chains using the LangChain framework, including `text-based decision chains`, `text-to-text`, `text-to-code`, `image-to-text`, and `text-to-image` generation. It leverages various models such as `llama3`, `codellama`, and `llava` from the `ChatOllama` suite and integrates OpenAI's `DALL-e` for image generation. The process involves creating prompt templates with specific rules and using these templates to process user queries through defined chains.
## Project Structure

- `app.py`: This is the main script that contains the streamlit app.
- `llm.py`: This file contains the lagnchain code for creating llm chains.


## Requirements

Ensure you have the following Python packages installed:

- streamlit
- langchain


You can install the required packages using the following command:

```sh
pip install -r requirements.txt
```

## Running the code
- To run the project, execute the `main.py` script:

```sh
streamlit run app.py
```

## Acknowledgements
This project is inspired by various tutorials and resources available for Multi-Agent Systems.