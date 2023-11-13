import azure.functions
from dotenv import load_dotenv
import logging
import json
load_dotenv()

import os
from utilities.helper import LLMHelper

def main(req: azure.functions.HttpRequest) -> str:
    print ("ApiQnA 1")
    # Get data from POST request
    try:
        req_body = req.get_json()
        if type(req_body) == str:
            logging.info("ApiQnA - body is not a json. Body: " + req_body)
            raise Exception("ApiQnA - body is not a json")

        logging.info ("ApiQnA str(req_body): " + str(req_body))
        logging.info ("ApiQnA str(type(req_body)): " + str(type(req_body)))
    except ValueError as error:
        logging.info("ApiQnA an exception occurred:" + str(error)) 
        # Si dejamos el pass, nos comemos el error, porque luego al inicializar el LLMHelper daría un error
        # Ya de paso quito el else, para que se ejecute siempre aunque de error esa parte
        #pass
        raise error
    #else:

    logging.info ("ApiQnA 2")
    question = req_body.get('question')
    history = req_body.get('history', [])
    custom_prompt = req_body.get('custom_prompt', "")
    custom_temperature = float(req_body.get('custom_temperature', os.getenv("OPENAI_TEMPERATURE", 0.0)))

    try:
        logging.info ("ApiQnA question: " + str(question))
        logging.info ("ApiQnA history: " + str(history))
        logging.info ("ApiQnA custom_prompt: " + str(custom_prompt))
        logging.info ("ApiQnA custom_temperature: " + str(custom_temperature))
    except: 
        pass

    # Create LLMHelper object
    k = os.getenv("AZURE_SEARCH_TOP_K_DOCS_FOR_CONTEXT", 4)
    logging.info ("AZURE_SEARCH_TOP_K_DOCS_FOR_CONTEXT = " + str(k))
    llm_helper = LLMHelper(custom_prompt=custom_prompt, temperature=custom_temperature, k = k)
    # Get answer
    logging.info ("ApiQnA 4")
    data = {}
    data['question'], data['response'], data['context'], data["sources"] = llm_helper.get_semantic_answer_lang_chain(question, history)
    # Return answer
    logging.info ("ApiQnA 5 Fin")
    return f'{data}'