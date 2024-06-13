from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import traceback
import signal
import time
import sys
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from __init__ import main_window, driver
from util import success_chime, show_popup, show_input_popup, load_config


# - - - NEW CONNECTION FUNCTIONS - - - 


def get_contact_box(driver):
    contact_box = driver.find_element(By.XPATH, '//div[contains(@class, "pv-top-card-v2-ctas")]')
    return contact_box

def get_profile_name(driver):
    full_name = driver.find_element(By.XPATH, '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text
    return full_name


def click_connect(driver):
    print('CLICKING CONNECT')
    full_name = get_profile_name(driver)
    contact_box = get_contact_box(driver)
    # Select the 'Connect' button
    xpath_expression = f'//button[contains(@aria-label, "Invite {full_name} to connect")]'
    connect_button = contact_box.find_elements(By.XPATH, xpath_expression)[1]
    time.sleep(2)
    connect_button.click()
        
    
def add_a_note(driver):
    # Add a note
    print('CLICKING ADD A NOTE')
    xpath_expression = '//button[@aria-label="Add a note"]'
    add_a_note_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=10)
    add_a_note_button.click()
    
    
def compose_new_connection(driver, name):
    print('COMPOSING MESSAGE')
    xpath_expression = '//textarea[@name="message"]'
    text_area = get_element(by=By.XPATH, selector=xpath_expression, timeout=6)
    introduction = load_introduction(name=name)
    text_area.send_keys(introduction)
    time.sleep(.5)
    
    print('CLICKING SEND')
    xpath_expression = '//button[@aria-label="Send invitation"]'
    send_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=6)
    send_button.click()

    
# - - - EXISTING CONNECTION FUNCTIONS - - - 
def click_message(driver):
    contact_box = get_contact_box(driver)
    
    # Select Message button
    xpath_expression = '//button[contains(@aria-label, "Message")]'
    message_buttons = contact_box.find_elements(By.XPATH, xpath_expression)
    for message_button in message_buttons:
        try:
            message_button.click()
            break
        except:
            pass
    time.sleep(3)
    
def check_already_sent(driver, name):
    intro = load_introduction(name=name)
    
    css_selector = "p.msg-s-event-listitem__body.t-14.t-black--light.t-normal"
    messages = driver.find_elements(By.CSS_SELECTOR, css_selector)
    sent_status = False
    for message in messages:
        if intro in message.text:
            print('You already contacted this person with your message! Skipping!')
            sent_status = True
            break
    if sent_status == False:
        print('Person has not yet been contacted!')
            
    return sent_status
    

        
def compose_message(driver, name):
    # Compose message
    print('Writing message to profile.')
    page_text = driver.find_element(By.XPATH, "/html/body").text
    if 'You haven’t received a response yet.' in page_text:
        print('You already contacted this person! Skipping...')
        return
        
    message_box = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Write a message…"]')
    introduction = load_introduction(name=name)
    message_box.send_keys(introduction)
    time.sleep(3)
    try:
        submit_button = driver.find_element(By.CLASS_NAME, 'msg-form__send-button')
        submit_button.click()
    except:
        message_box.send_keys(Keys.RETURN)
    print('Message has been sent to profile')
    time.sleep(2)
        
def close_all_chats(driver):
    class_name = "msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"
    xpath_expression = f"//button[contains(@class, '{class_name}')]"

    close_buttons = driver.find_elements(By.XPATH, xpath_expression)
    for close_button in close_buttons:
        close_button.click()
        time.sleep(1)
        
        
# - - - PROFILE DISCOVERY / NAVIGATION - - - 
def scroll_to_element(driver, element):
    # Use JavaScript to scroll the element into view
    #driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    
def scroll_to_bottom(driver):
    # Use JavaScript to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
def click_next(driver):
    next_page_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
    scroll_to_element(driver, next_page_button)
    next_page_button.click()
    
def get_profile_links(driver):
    people_box = driver.find_element(By.CSS_SELECTOR, 'ul[class="reusable-search__entity-result-list list-style-none"]')
    all_links = people_box.find_elements(By.TAG_NAME, 'a')
    profile_links = [link.get_attribute('href') for link in all_links if 'https://www.linkedin.com/in/' in link.get_attribute('href')]
    profile_links = list(set(profile_links))
    print(f'Found {len(profile_links)} profiles!')
    return profile_links

def connection_status(driver):
    contact_box = driver.find_element(By.XPATH, '//div[contains(@class, "pv-top-card-v2-ctas")]')
    html = contact_box.get_attribute('outerHTML')
    if 'Remove your connection' in html:
        print('You are ALREADY CONNECTED to this profile!')
        return 'CONNECTED'
    elif 'Pending, click to withdraw' in html:
        print('Your connection is PENDING with this profile!')
        return 'PENDING'
    else:
        print('You are NOT YET CONNECTED to this profile!')
        return 'NOT CONNECTED'
    
def load_introduction(name, path='./introduction.txt'):
    with open(path, 'r') as file:
        file_content = file.read()
    intro = file_content.replace('FIRST_NAME', name)
    if len(intro) > 300:
        print(f'ERROR:\nYour introduction is too long ({len(intro)} chars).\nShorten your intro to no more than 300 characters and restart the bot.')
        exit()
        
    return intro
    
def introduce(driver, profile_link):
    close_all_chats(driver)
    first_name = get_profile_name(driver).split(' ')[0]
    print(f'NEW PROFILE: {first_name.upper()}')
    status = connection_status(driver)
    if status == 'NOT CONNECTED':
        try:
            click_connect(driver)
            add_a_note(driver)
            compose_new_connection(driver, first_name)
        except:
            print(f'WARNING! could not connect to {first_name}')
            pass
    elif status == 'PENDING':
        print('Skipping introduction! Your connection is already pending.')
    else:
        print('Skipping message, already connected')
        # click_message(driver)
        # if check_already_sent(driver, first_name) == False:
        #     compose_message(driver, first_name)
    close_all_chats(driver)




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




# - - - - - - -  M A I N   E X E C U T I O N   S T A R T - - - - - - - - - 
print('\n - - - LINKEDINBOT - - - \n')

config = load_config()
USERNAME = config['Email']
PASSWORD = config['Password']

print('- - ENTER PEOPLE SEARCH QUERY - -')
INDUSTRY = show_input_popup(title="JOB QUERY", message="Enter and submit your recruiter search query.\n E.g.: data science recruiter, google recruiter etc.", password=False)
INDUSTRY = INDUSTRY.strip()
# Optional: You can add additional actions here, such as interacting with elements on the page
time.sleep(3)
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

# Enter search query in LinkedIn search
search_field = get_element(by=By.CSS_SELECTOR, selector='input[placeholder="Search"]', timeout=5)
if not search_field:
    show_popup(message='Complete security challenge if necessary and press CONTINUE.\n\n(If you are already on the LinkedIn homepage, just press CONTINUE): ')
    search_field = get_element(by=By.CSS_SELECTOR, selector='input[placeholder="Search"]', timeout=5)
    
# - - LINKEDIN HOMEPAGE FEED - -
# Enter search query in LinkedIn search
search_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
search_field.send_keys(INDUSTRY)
search_field.send_keys(Keys.RETURN)
time.sleep(5)


# - - PEOPLE RESULTS PAGE - - 
# Select the 'People' search filter
# Wait for page to load
xpath_expression = '.artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--2.search-reusables__filter-pill-button'
get_element(by=By.CSS_SELECTOR, selector=xpath_expression, timeout=10) 
# Select the 'Jobs' search filter 
filter_buttons = driver.find_elements(By.CSS_SELECTOR, xpath_expression)
for button in filter_buttons:
    if 'People' in button.text:
        button.click()
        break

# Select the 'Actively Hiring' search filter if user is a LinkedIn Premium member
xpath_expression = '//button[@id="searchFilter_activelyHiringForJobTitles"]'
actively_hiring_filter = get_element(by=By.XPATH, selector=xpath_expression, timeout=5)
if actively_hiring_filter:
    actively_hiring_filter.click()
else:
    print('ALERT: Could not click Actively Hiring Filter')

# Start messaging people
try:
    query = INDUSTRY.replace(" ", '%20')
    page = 0
    while True:
        page += 1
        sid = driver.current_url.split('=')[-1]
        url = f"https://www.linkedin.com/search/results/people/?activelyHiringForJobTitles=%5B%22-100%22%5D&keywords={query}&origin=FACETED_SEARCH&page={page}&sid={sid}"
        driver.get(url) # Go to next page.
        time.sleep(5)
        connect_buttons = driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Invite")]')
        for button in connect_buttons:
            scroll_to_element(driver, button)
            name = button.get_attribute("aria-label").split(' ')[1]
            time.sleep(.5)
            button.click()
            add_a_note(driver)
            time.sleep(.5)
            compose_new_connection(driver, name)
            time.sleep(1)
        #click_next(driver)
        time.sleep(5)
except Exception as e:
    print(e)
    show_popup("ERROR: something went wrong.\nPress 'Continue' to exit program.")