from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import tkinter
import traceback
import signal
import time
import sys
import os

from __init__ import main_window, driver
from util import success_chime, show_popup, show_input_popup, load_config


print('\n - - - LINKEDINBOT - - - \n')

config = load_config()
USERNAME = config['Email']
PASSWORD = config['Password']


INDUSTRY = show_input_popup(title="Job Search Query", message="Enter and submit your job search query.\nE.g.: 'data scientist', 'sales executive, etc.")
print('')

def wait():
    input('Press enter to continue: ')


def load_introduction(name, path='./introduction.txt'):
    with open(path, 'r') as file:
        file_content = file.read()
    intro = file_content.replace('FIRST_NAME', name)
    if len(intro) > 300:
        print(f'ERROR:\nYour introduction is too long ({len(intro)} chars).\nShorten your intro to no more than 300 characters and restart the bot.')
        exit()
        
    return intro


# Open the website
url = 'https://www.linkedin.com'
print(f'\nOpening: {url}\n')
driver.get(url)

# Optional: You can add additional actions here, such as interacting with elements on the page
time.sleep(3)

# - - LOG IN PAGE - -
# Enter username
username_field = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
username_field.send_keys(USERNAME)
time.sleep(3)

# Enter password
password_field = driver.find_element(By.ID, 'session_password')
password_field.send_keys(PASSWORD)
time.sleep(1)

# Submit sign-in credentials
sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]')
sign_in_btn.click()

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
easy_apply_clicked = False
for i in range(5):
    try:
        xpath_expression = '//button[@aria-label="Easy Apply filter."]'
        actively_hiring_filter = driver.find_element(By.XPATH, xpath_expression)
        actively_hiring_filter.click()
        easy_apply_clicked = True
        time.sleep(3)
        break
    except:
        time.sleep(3)

if not easy_apply_clicked:
    show_popup(message='Manually select the easy apply filter press CONTINUE: ')
        

# Location filter 
show_popup(message='Manually select and apply any additional job search filters in the browser press CONTINUE:')
    
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
            #print(jobs_list.get_attribute('outerHTML'))

            xpath_expression = '//a[@class="disabled ember-view job-card-container__link job-card-list__title"]'
            job_links = jobs_container.find_elements(By.XPATH, xpath_expression)
            print(f'{len(job_links)} jobs discovered.\n')
            if len(job_links) >= 25:
                return job_links

            #scroll_to_element(driver, job_links[-1])
            for job in job_links:
                driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(.5)
            driver.execute_script("arguments[0].scrollIntoView();", job_links[0])
        return job_links
    except Exception as e:
        print('')
        print('- - ERROR: SOMETHING WENT WRONG - - ')
        print(e)
        print(traceback.format_exc())
        print('')


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
    easy_apply_window = driver.find_element(By.XPATH, xpath_expression)
    form_element = driver.find_element(By.TAG_NAME, "form")
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

                questions = [q.text for q in form_element.find_elements(By.TAG_NAME, "label")]
                fields = form_element.find_elements(By.TAG_NAME, "input")
                
                # Review the application
                click_next(driver)
                time.sleep(2)
                if check_window(driver=driver, phrase='Additional Questions') and not check_window(driver=driver, phrase='Review your application'):
                    raise Exception
            except:
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

pages = get_nav_pages(driver)
    
try:
    num_pages = len(pages)
    for i in range(num_pages):
        pages = get_nav_pages(driver)
        job_links = expose_jobs(driver)
        for link in job_links:
            scroll_to_element(driver, link)
            time.sleep(2)
            link.click()

            xpath_expression = '//div[@id="job-details"]'
            job_description = driver.find_element(By.XPATH, xpath_expression)
            #print(job_description.text[:20])
            time.sleep(2.3)

            try:
                xpath_expression = '//button[@class="jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view"]'
                easy_apply_button = driver.find_element(By.XPATH, xpath_expression)
                easy_apply_button.click()
                time.sleep(4)
            except:
                continue

            easy_apply(driver)
        scroll_to_element(driver, pages[i+1])
        time.sleep(2)
        pages[i+1].click()
        print("\nALERT: Continuing to next page of job results.")
        time.sleep(5)
    
except Exception as e:
    print('')
    print('- - ERROR: SOMETHING WENT WRONG - - ')
    print(e)
    print(traceback.format_exc())
    print('')
    
play_beep()
response = input('Do you want to quit? y/n: ')
if response == 'y':
    driver.quit()