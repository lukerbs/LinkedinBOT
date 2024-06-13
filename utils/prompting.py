import os
import json



def load_prompt(prompt):
    path = f"{os.path.dirname(__file__)}/prompts/{prompt}"
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_json(string):
    json_string = string[string.find("{") : string.find("}") + 1]
    json_data = json.loads(json_string)
    return json_data

def question_prompt(questions: list[dict], resume:str, job_description:str):
    prompt = load_prompt('app_question.txt')
    question_str = ''
    for i, question in enumerate(questions):
        if question['type'] == 'text':
            question_str += f"QUESTION {i} (text response): {question['question']}\n"
        elif question['type'] == 'text-numeric':
            question_str += f"QUESTION {i} (numeric response): {question['question']}\n"
        elif question['type'] in ['radio', 'dropdown']:
            question_str += f"QUESTION {i} (select one): {question['question']}\n"
            options_str = {}
            for j, option in enumerate(question['options']):
                options_str[j] = option['label']
            question_str += f"\t- QUESTION {i} OPTIONS: {options_str}\n"
    
    print(question_str)

    prompt = prompt.replace("APPLICATION_QUESTIONS", question_str)
    prompt = prompt.replace("RESUME", resume)
    prompt = prompt.replace("JOB_DESCRIPTION", job_description)
    return prompt
    
