import azure.functions
from dotenv import load_dotenv
load_dotenv()

import os
from utilities.helper import LLMHelper

def main(req: azure.functions.HttpRequest) -> str:
    print ("ApiQnA 1")
    # Get data from POST request
    try:
        req_body = req.get_json()
    except ValueError as error:
        print("ApiQnA an exception occurred:", error) 
        pass
    else:
        print ("ApiQnA 2")
        question = req_body.get('question')
        history = req_body.get('history', [])
        custom_prompt = req_body.get('custom_prompt', "")
        custom_temperature = float(req_body.get('custom_temperature', os.getenv("OPENAI_TEMPERATURE", 0.7)))
    print ("ApiQnA 3")
    # Create LLMHelper object
    llm_helper = LLMHelper(custom_prompt=custom_prompt, temperature=custom_temperature)
    # Get answer
    print ("ApiQnA 4")
    data = {}
    data['question'], data['response'], data['context'], data["sources"] = llm_helper.get_semantic_answer_lang_chain(question, history)
    # Return answer
    print ("ApiQnA 5 Fin")
    return f'{data}'