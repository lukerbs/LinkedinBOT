import os
import json
from .ai import chatgpt



def load_prompt(prompt):
    path = f"{os.path.dirname(__file__)}/prompts/{prompt}"
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_json(string):
    json_string = string[string.find("{") : string.find("}") + 1]
    json_data = json.loads(json_string)
    return json_data

def question_prompt(questions: list[dict], job_description:str):
    with open(f'{os.path.dirname(__file__)}/../resume.txt', "r") as file:
        resume = file.read()
    
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

def summarize_job(job_description: str) -> str:
    prompt = load_prompt("summarize_jd.txt")
    prompt = prompt.replace("JOB_DESCRIPTION", job_description)
    job_overview = chatgpt(prompt=prompt)
    return job_overview

def customize_resume(job_description: str, mode="HTML") -> str:
    with open(f'{os.path.dirname(__file__)}/../resume.txt', "r") as file:
        resume = file.read()
        resume = "".join([f"\t{line.strip()}\n" for line in resume.splitlines()])

    job_description = "".join([f"\t{line.strip()}\n" for line in job_description.splitlines()])

    if mode == "HTML":
        prompt = load_prompt('custom_resume_html.txt')
    elif mode == "markdown":
        prompt = load_prompt('custom_resume_md.txt')

    prompt = prompt.replace("MY_RESUME", resume)
    prompt = prompt.replace("JOB_DESCRIPTION", job_description)
    custom_resume = chatgpt(prompt=prompt)
    return custom_resume



    
