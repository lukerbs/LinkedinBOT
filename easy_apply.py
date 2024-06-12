from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import traceback
from pprint import pprint
import time
import atexit

import openai

CHATGPT = None
client = openai.OpenAI(api_key=CHATGPT)
def chatgpt(query:str, model='gpt-4-turbo-preview', max_tokens=None):
    # select model from ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview', 'gpt-4-32k', 'gpt-4-1106-preview']
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens, #4000
        messages=[
            {"role": "user", "content": query}
        ]
    )

    response = completion.choices[0].message.content

    return response

from __init__ import driver
from util import success_chime, show_popup, show_input_popup, load_config, cleanup

atexit.register(cleanup)

print('\n - - - LINKEDINBOT - - - \n')

config = load_config()
USERNAME = config['Email']
PASSWORD = config['Password']


INDUSTRY = show_input_popup(title="Job Search Query", message="Enter and submit your job search query.\nE.g.: 'data scientist', 'sales executive, etc.")
print('')

def wait():
    input('Press enter to continue: ')

def get_element(by, selector, timeout):
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.presence_of_element_located((by, selector)))
        return element
    except TimeoutException:
        print(f'TimeoutException: Could not find element within {timeout} seconds.\n')
        return None


def check_sign_in_page():
    xpath_expression = '//a[@data-test-id="home-hero-sign-in-cta"]'
    sign_in_btn = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
    return sign_in_btn
    
def scroll_to_element(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

# Load all job links
def expose_jobs(driver):
    print('\nALERT: Please wait. Scanning for jobs applications.')
    try:
        for i in range(5):
            xpath_expression = '//ul[@class="scaffold-layout__list-container"]'
            jobs_container = driver.find_element(By.XPATH, xpath_expression)

            xpath_expression = '//a[@class="disabled ember-view job-card-container__link job-card-list__title job-card-list__title--link"]'
            job_links = jobs_container.find_elements(By.XPATH, xpath_expression)

            print(f'Job Links Discovered: {len(job_links)}\n')
            if len(job_links) >= 16:
                # Return job links if reached 24 links.
                return job_links
            

            for job in job_links:
                # Scroll to each link in list down to the bottom of the list.
                driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(.5)
            
            # Scroll to top of list.
            driver.execute_script("arguments[0].scrollIntoView();", job_links[0])

        return job_links
    except Exception as e:
        print(f"WARNING: No job links discovered.")
        return None


def check_window(driver, phrase):
    xpath_expression = '//div[@class="jobs-easy-apply-content"]'
    easy_apply_window = driver.find_element(By.XPATH, xpath_expression)
    if phrase in easy_apply_window.text:
        return True
    else:
        return False
    
def click_next(driver):
    xpath_expression = '//button[@aria-label="Continue to next step"]'
    next_button = driver.find_element(By.XPATH, xpath_expression)
    scroll_to_element(driver, next_button)
    next_button.click()
    
def click_review(driver):
    xpath_expression = '//button[@aria-label="Review your application"]'
    review_button = driver.find_element(By.XPATH, xpath_expression)
    review_button.click()
    
def submit_application(driver):
    xpath_expression = '//button[@aria-label="Submit application"]'
    submit_button = driver.find_element(By.XPATH, xpath_expression)
    scroll_to_element(driver, submit_button)
    time.sleep(2)
    submit_button.click()
    
def custom_q_form(driver):
    xpath_expression = '//div[@class="jobs-easy-apply-content"]'
    easy_apply_window = get_element(by=By.XPATH, selector=xpath_expression, timeout=5)
    form_element = easy_apply_window.find_element(By.TAG_NAME, "form")
    return form_element

def close_application(driver):
    xpath_expression = '//button[@aria-label="Dismiss"]'
    close_button = driver.find_element(By.XPATH, xpath_expression)
    close_button.click()
    
def discard_application(driver):
    xpath_expression = '//button[@data-control-name="discard_application_confirm_btn"]'
    discard_button = driver.find_element(By.XPATH, xpath_expression)
    discard_button.click()
    


def field_requirement(element):
    requirement = element.get_attribute("aria-describedby")
    if 'numeric' in requirement:
        return 'numeric'
    else:
        return 'Unknown'
    
def application_error_close(driver):
    close_application(driver)
    time.sleep(3)
    discard_application(driver)
    time.sleep(3)
    return
    
def get_answer(question):
    return

def easy_apply(driver):
    while True:
        if check_window(driver=driver, phrase='Contact info') and not check_window(driver=driver, phrase='Review your application'):
            try:
                submit_application(driver)
                time.sleep(2)
                close_application(driver)
                return
            except:
                pass
            #print('You are in the contact section')
            click_next(driver)
            time.sleep(4)
            continue
        elif check_window(driver=driver, phrase='Voluntary self identification') and not check_window(driver=driver, phrase='Review your application'):
            #print('You are in the Self Identification section')
            click_next(driver)
            time.sleep(3)
            continue
        elif check_window(driver=driver, phrase='Be sure to include an updated resume') and not check_window(driver=driver, phrase='Review your application'):
            #print('You are on the resume section')
            try:
                click_next(driver)
                time.sleep(3)
                continue
            except:
                click_review(driver)
                time.sleep(3)
                continue
        elif check_window(driver=driver, phrase='Work authorization') and not check_window(driver=driver, phrase='Review your application'):
            #print('You are on the work authorization section')
            try:
                click_next(driver)
                time.sleep(3)
                continue
            except:
                click_review(driver)
                time.sleep(3)
                continue
        elif check_window(driver=driver, phrase='Additional Questions') and not check_window(driver=driver, phrase='Review your application'):
            try:
                #print('You are on the additional questions section')
                
                form_element = custom_q_form(driver)

                # Get text input questions
                text_questions = []
                text_input_labels = [q_label for q_label in form_element.find_elements(By.TAG_NAME, "label") if q_label.get_attribute("class") == "artdeco-text-input--label"]
                for label in text_input_labels:
                    question = label.text
                    field_id = label.get_attribute("for")
                    field = form_element.find_element(By.ID, field_id)
                    if field.get_attribute("value"):
                        print(f"COMPLETE: '{question}'")
                        continue

                    if "numeric" in field.get_attribute("id"):
                        field_type = "text-numeric"
                    else:
                        field_type = "text"
                    
                    field_data = {
                        "question": question,
                        "type": field_type,
                        "element": field
                    }
                    pprint(field_data)
                    text_questions.append(field_data)

                # Get radio button input sections
                xpath_expression = '//fieldset[@data-test-form-builder-radio-button-form-component="true"]'
                radio_btn_sections = form_element.find_elements(By.XPATH, xpath_expression)
                radio_btn_questions = []
                for radio_section in radio_btn_sections:
                    section_completed = False
                    question = radio_section.find_element(By.XPATH, '//span[@aria-hidden="true"]').text

                    radio_btn_labels = radio_section.find_elements(By.TAG_NAME, "label")
                    options = []
                    for option in radio_btn_labels:
                        btn_id = option.get_attribute("for")
                        radio_option_btn = radio_section.find_element(By.ID, btn_id)
                        if radio_option_btn.is_selected():
                            print(f"QUESTION COMPLETED (skipping): {question}")
                            section_completed = True
                            break

                        else:
                            option_info = {
                                "label": option.get_attribute("data-test-text-selectable-option__label"),
                                "element": option#radio_option_btn
                            }
                            options.append(option_info)
                    
                    if not section_completed:
                        question_data = {
                            "question": question,
                            "type": "radio",
                            "options": options
                        }
                        pprint(question_data)
                        radio_btn_questions.append(question_data)

                # Get dropdow menu input sections
                drop_down_questions = []
                drop_down_menus = form_element.find_elements(By.TAG_NAME, 'select')
                for drop_down in drop_down_menus:
                    drop_down_id = drop_down.get_attribute("id")
                    question = form_element.find_element(By.XPATH, f'//label[@for="{drop_down_id}"]').text
                    print(question)

                    section_complete = False
                    options = drop_down.find_elements(By.TAG_NAME, "option")
                    options_data = []
                    for option in options:
                        print(option.text)
                        if option.is_selected() and option.get_attribute("value") != "Select an option":
                            section_complete = True
                            break

                        value = option.get_attribute("value")
                        if value != "Select an option":
                            option_details = {
                                "label": value,
                                "element": option,
                            }
                            options_data.append(option_details)

                    if not section_complete:
                        question_data = {
                            "question": question,
                            "element": drop_down,
                            "type": "dropdown",
                            "options": options_data
                        }
                        drop_down_questions.append(question_data)

                
                unanswered_questions = drop_down_questions + radio_btn_questions + text_questions
                pprint(unanswered_questions)

                with open('./resume.txt', "r") as file:
                    resume = file.read()

                for question in unanswered_questions:
                    scroll_to_element(driver, question['element'])
                    prompt = f"I need help filling out a job application. Based on my resume (below) please help me answer this question on the application (only return the answer):"
                    prompt = f"{prompt}\nQUESTION: '{question['question']}\n'"
                    prompt = f"{prompt}Additional Instructions: if you're not sure about an answer, give your best guess.\n"

                    if question['type'] == "text":
                        prompt = f"{prompt}RESUME:\n{resume}"
                        response = chatgpt(prompt)
                        print(f"ANWSER: {response}")
                        question['element'].send_keys(response)
                        

                    elif question['type'] == "text-numeric":
                        prompt = f"{prompt}\n Also, only return the answer as a number."
                        prompt = f"{prompt}RESUME:\n{resume}"
                        response = chatgpt(prompt)
                        print(f"ANWSER: {response}")
                        question['element'].send_keys(response)
                    elif question['type'] == "radio":
                        prompt = f"{prompt}\nJust return the integer number for the option that is the best answer and nothing else.\n"
                        for i,option in enumerate(question['options']):
                            prompt = f"{prompt}OPTION {i}: {option['label']}\n"
                        
                        prompt = prompt + '\n'
                        prompt = f"{prompt}RESUME:\n{resume}"
                        response = chatgpt(prompt)
                        print(f"ANWSER: {response}")
                        question['options'][int(response)]['element'].click()
                    elif question['type'] == "dropdown":
                        question['element'].click()
                        prompt = f"{prompt}\nJust return the integer number for the option that is the best answer and nothing else.\n"
                        for i,option in enumerate(question['options']):
                            prompt = f"{prompt}OPTION {i}: {option['label']}\n"
                        prompt = prompt + '\n'
                        prompt = f"{prompt}RESUME:\n{resume}"
                        response = chatgpt(prompt)
                        print(f"ANWSER: {response}")
                        time.sleep(1)
                        question['options'][int(response)]['element'].click()
                    time.sleep(1)
                
                # Review the application
                click_next(driver)
                time.sleep(2)
                if check_window(driver=driver, phrase='Additional Questions') and not check_window(driver=driver, phrase='Review your application'):
                    raise Exception
            except Exception as e:
                print(traceback.format_exc())
                try:
                    click_review(driver)
                    time.sleep(2)
                    if check_window(driver=driver, phrase='Review your application'):
                        continue
                except:
                    pass
                show_popup(message='Manually complete section and press CONTINUE:')
                time.sleep(1)
                try:
                    click_next(driver)
                    time.sleep(3)
                    continue
                except:
                    click_review(driver)
                    time.sleep(3)

        elif check_window(driver=driver, phrase='Review your application'):
            time.sleep(1)
            #print('You are on the application review section')
            submit_application(driver)
            print('\nALERT: Your application has successfully been submitted!')
            success_chime()
            time.sleep(2)
            close_application(driver)
            return

        else:
            try:
                time.sleep(1)
                click_next(driver)
                time.sleep(2)
            except:
                try:
                    click_review(driver)
                    time.sleep(2)
                except:
                    pass
            show_popup(message='Application section not recognized.\nComplete application section and press CONTINUE:')
            try:
                click_next(driver)
                time.sleep(2)
            except:
                pass
        
# Pagination
def get_nav_pages(driver):
    xpath_expression = '//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]'
    pagination_container = driver.find_element(By.XPATH, xpath_expression)
    scroll_to_element(driver, pagination_container)
    pages = pagination_container.find_elements(By.CSS_SELECTOR, "li[data-test-pagination-page-btn]")
    return pages



# - - - - - - -  M A I N   E X E C U T I O N   S T A R T - - - - - - - - - 
# - - LOG IN PAGE - -
# Enter username
version_2_btn = check_sign_in_page()
if not version_2_btn:
    print(f"Sign in version 1")
    username_field = get_element(by=By.CSS_SELECTOR, selector='input[autocomplete="username"]', timeout=3)
    username_field.send_keys(USERNAME)
    time.sleep(1)

    password_field = get_element(by=By.ID, selector='session_password', timeout=3)
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Submit sign-in credentials
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]')
    sign_in_btn.click()
else:
    print(f"Sign in version 2")
    version_2_btn.click()
    username_field = get_element(by=By.CSS_SELECTOR, selector='input[id="username"]', timeout=3)
    username_field.send_keys(USERNAME)
    time.sleep(1)

    password_field = get_element(by=By.ID, selector='password', timeout=3)
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Submit sign-in credentials
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="btn__primary--large from__button--floating"]')
    sign_in_btn.click()

# - - SECURITY CHALLENGE - -
# Wait for security challenge 
show_popup(message='Complete security challenge if necessary and press CONTINUE.\n\n(If you are already on the LinkedIn homepage, just press CONTINUE): ')
time.sleep(3)

# - - LINKEDIN HOMEPAGE FEED - -
# Enter search query in LinkedIn search
search_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
search_field.send_keys(INDUSTRY)
search_field.send_keys(Keys.RETURN)
time.sleep(5)


#- - PEOPLE RESULTS PAGE - - 
# Select the 'Jobs' search filter 
try:
    # Apply people filter 
    filter_buttons = driver.find_elements(By.CSS_SELECTOR, '.artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--2.search-reusables__filter-pill-button')
    jobs_button = None
    for button in filter_buttons:
        if 'Jobs' in button.text:
            jobs_button = button
            break
    if jobs_button:
        jobs_button.click()
    else:
        print('Could not find jobs button')
        
except Exception as e:
    print(f'ERROR: {e}')
    
# Select the 'Easy Apply' filter
xpath_expression = '//button[@aria-label="Easy Apply filter."]'
actively_hiring_filter = get_element(by=By.XPATH, selector=xpath_expression, timeout=5)
if actively_hiring_filter:
    actively_hiring_filter.click()
    easy_apply_clicked = True
else:
    easy_apply_clicked = False

if not easy_apply_clicked:
    show_popup(message='Manually select the easy apply filter press CONTINUE: ')
        
# Manually add any additional job search filters.
show_popup(message='Manually select and apply any additional job search filters in the browser press CONTINUE:')

pages = get_nav_pages(driver)
try:
    num_pages = len(pages)
    for i in range(num_pages):
        pages = get_nav_pages(driver)
        job_links = expose_jobs(driver)
        for link in job_links:
            scroll_to_element(driver, link)
            #time.sleep(2)
            link.click()

            xpath_expression = '//div[@id="job-details"]'
            job_description = driver.find_element(By.XPATH, xpath_expression)
            #print(job_description.text[:20])
            #time.sleep(2.3)

            # Click Job Application
            xpath_expression = '//button[@class="jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view"]'
            easy_apply_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
            if not easy_apply_button:
                continue
            easy_apply_button.click()
            time.sleep(4)

            easy_apply(driver)

        # Go to next page of job search results
        scroll_to_element(driver, pages[i+1])
        time.sleep(2)
        pages[i+1].click()
        print("\nALERT: Continuing to next page of job results.")
        time.sleep(5)
    
except Exception as e:
    message = 'An unexpected error occurred.\nPress continue to close the program. Restart the program to resume.'
    show_popup(message=message, error=True)
    print('')
    print('- - ERROR: SOMETHING WENT WRONG - - ')
    print(traceback.format_exc())
    print('')