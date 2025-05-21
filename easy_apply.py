from pprint import pprint
import traceback
import atexit
import time
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enum import Enum, auto

from __init__ import driver
from util import success_chime, show_popup, show_input_popup, load_config, cleanup
from utils.prompting import question_prompt, extract_json
from utils.ai import chatgpt
from utils.helpers import str_to_bool

atexit.register(cleanup)
load_dotenv()


print("\n - - - LINKEDINBOT - - - \n")
SKIP_EDUCTATION_FORM = str_to_bool(os.getenv("SKIP_EDUCATION_FORM"))
config = load_config()
USERNAME = config["Email"]
PASSWORD = config["Password"]


def wait():
    input("Press enter to continue: ")


def get_element(by, selector, timeout):
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.presence_of_element_located((by, selector)))
        return element
    except TimeoutException:
        print(f"TimeoutException: Could not find element within {timeout} seconds.\n")
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
    print("\nALERT: Please wait. Scanning for jobs applications.")
    try:
        for _ in range(5):
            job_links = driver.find_elements(By.CSS_SELECTOR, "ul div[data-job-id][data-view-name='job-card']")

            print(f"Job Links Discovered: {len(job_links)}\n")
            if len(job_links) >= 24:
                # Return job links if reached 24 links.
                return job_links

            for job in job_links:
                # Scroll to each link in list down to the bottom of the list.
                driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(0.05)

            # Scroll to top of list.
            driver.execute_script("arguments[0].scrollIntoView();", job_links[0])

        return job_links
    except Exception as e:
        print(f"WARNING: No job links discovered.")
        return None


def check_education_page(form_element):
    xpath_expression = '//span[@class="t-bold"]'
    elements = form_element.find_elements(By.XPATH, xpath_expression)
    for element in elements:
        if element.text == "Education":
            print(f"ALERT: Skipping education section!")
            xp = '//select[@name="month"]'
            menu = get_element(by=By.XPATH, selector=xp, timeout=3)
            if menu:
                return True
    print(f"ALERT: Not skipping education section!")
    return False


def attempt_skip():
    try:
        click_next(driver)
        time.sleep(1)
        return
    except:
        pass
    try:
        click_review(driver)
        time.sleep(1)
        return
    except:
        pass


def get_form_section_title(driver):
    xpath_expression = '//div[@class="artdeco-modal__content jobs-easy-apply-modal__content p0 ember-view"]//form//h3[@class="t-16 t-bold"]'
    title = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
    if title:
        return title.text
    else:
        title = driver.find_element(
            By.XPATH,
            "//div[@data-test-modal-id='easy-apply-modal' and contains(@class, 'artdeco-modal-overlay')]"
            + "//h3[contains(@class, 't-18')]",
        )
        if title:
            return title.text
        else:
            return None


# def check_window(driver, phrase):
#     xpath_expression = '//div[@class="jobs-easy-apply-content"]'
#     easy_apply_window = driver.find_element(By.XPATH, xpath_expression)
#     if phrase in easy_apply_window.text:
#         return True
#     else:
#         return False


def click_next(driver):
    print("Searching for next button...")
    # xpath_expression = '//button[@aria-label="Continue to next step"]'
    next_button = driver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']")

    # next_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
    if not next_button:
        print("WARNING: No next button found.")
    else:
        print(f"Next button found!")

    print(f"Scrolling to next button...")
    scroll_to_element(driver, next_button)
    body = get_element(by=By.TAG_NAME, selector="body", timeout=5)
    page_text = body.text
    print(f"Clicking next button...")
    next_button.click()
    body = get_element(by=By.TAG_NAME, selector="body", timeout=5)
    page_text_new = body.text
    if page_text == page_text_new:
        return False
    else:
        return True


def click_review(driver):
    xpath_expression = '//button[@aria-label="Review your application"]'
    review_button = driver.find_element(By.XPATH, xpath_expression)
    body = get_element(by=By.TAG_NAME, selector="body", timeout=5)
    page_text = body.text
    scroll_to_element(driver, review_button)
    review_button.click()
    body = get_element(by=By.TAG_NAME, selector="body", timeout=5)
    page_text_new = body.text
    if page_text == page_text_new:
        return False
    else:
        return True


def submit_application(driver):
    xpath_expression = '//button[@aria-label="Submit application"]'
    submit_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
    scroll_to_element(driver, submit_button)
    submit_button.click()
    print("\nALERT: Your application has successfully been submitted!")
    success_chime()
    time.sleep(2)
    close_application(driver)
    time.sleep(2)


def custom_q_form():
    try:
        # xpath_expression = '//div[@class="jobs-easy-apply-content"]'
        # easy_apply_window = get_element(by=By.XPATH, selector=xpath_expression, timeout=3)
        css_expression = "div[data-test-modal][role='dialog'][class='artdeco-modal artdeco-modal--layer-default jobs-easy-apply-modal'][aria-labelledby='jobs-apply-header']"
        easy_apply_window = driver.find_element(By.CSS_SELECTOR, css_expression)

        form_element = easy_apply_window.find_element(By.TAG_NAME, "form")
        return form_element
    except:
        return False


def close_application(driver):
    xpath_expression = '//button[@aria-label="Dismiss"]'
    close_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=6)
    if close_button:
        close_button.click()


def discard_application(driver):
    xpath_expression = '//button[@data-control-name="discard_application_confirm_btn"]'
    discard_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=6)
    if discard_button:
        discard_button.click()


def field_requirement(element):
    requirement = element.get_attribute("aria-describedby")
    if "numeric" in requirement:
        return "numeric"
    else:
        return "Unknown"


def application_error_close(driver):
    close_application(driver)
    time.sleep(1)
    discard_application(driver)
    time.sleep(1)
    return


def easy_apply(driver, job_description):
    failures = 0
    print("\n=== Starting Easy Apply Process ===")
    while True:
        print(f"Current form section: {get_form_section_title(driver)}")
        if failures > 1:
            print(f"WARNING: {failures} Consecutive failures.")
        # Quit current application if gets stuck.
        if failures > 1:
            print(f"WARNING: loop {failures}")

        if failures >= 10:
            print(f"\n- - STUCK IN A LOOP - - ")
            print(f"Discarding application.")
            application_error_close(driver)
            return

        print("\n--- Checking Contact Info Section ---")
        if (
            get_form_section_title(driver) == "Contact info"
        ):  # and not check_window(driver=driver, phrase='Review your application'):
            print("Found Contact Info section")
            if click_next(driver):
                print("Successfully clicked next")
                failures = 0
            else:
                print("Failed to click next")
                try:
                    print("Attempting to submit application...")
                    submit_application(driver)
                    print("Application submitted successfully!")
                    return
                except Exception as e:
                    print(f"Submit failed, trying next button. Error: {str(e)}")

        else:
            print(f"Not contact info section...")

        print("\n--- Checking Self Identification Section ---")
        if (
            get_form_section_title(driver) == "Voluntary self identification"
        ):  # and not check_window(driver=driver, phrase='Review your application'):
            print("Found Self Identification section")
            if not click_next(driver):
                print("Failed to click next in Self Identification")
                failures += 1
            else:
                print("Successfully clicked next in Self Identification")
                failures = 0
        else:
            print(f"Not self identification section...")

        print("\n--- Checking Resume Section ---")
        if (
            get_form_section_title(driver) == "Be sure to include an updated resume"
        ):  # and not check_window(driver=driver, phrase='Review your application'):
            print("Found Resume section")
            try:
                if click_next(driver):
                    print("Successfully clicked next in Resume section")
                    failures = 0
                else:
                    print("Failed to click next in Resume section")
                    failures += 1
                time.sleep(1)
            except Exception as e:
                print(f"Error in Resume section: {str(e)}")
                failures += 1
                pass
        else:
            print(f"Not resume section...")

        print("\n--- Checking Work Authorization Section ---")
        if (
            get_form_section_title(driver) == "Work authorization"
        ):  # and not check_window(driver=driver, phrase='Review your application'):
            print("Found Work Authorization section")
            try:
                if click_next(driver):
                    print("Successfully clicked next in Work Authorization")
                    failures = 0
                else:
                    print("Failed to click next in Work Authorization")
                    failures += 1
                time.sleep(1)
            except Exception as e:
                print(f"Error in Work Authorization: {str(e)}")
                failures += 1
                pass
        else:
            print(f"Not work authorization section...")

        print("\n--- Checking Custom Form Section ---")
        form_element = custom_q_form()
        if form_element and not get_form_section_title(driver) == "Review your application":
            print("Found Custom Form section")
            try:
                if not "additional" in form_element.text.lower() or "cover letter" not in form_element.text.lower():
                    print("Processing form questions...")
                    try:
                        if click_next(driver):
                            print("Successfully clicked next in form section")
                            failures = 0
                        else:
                            print("Failed to click next in form section")
                            failures += 1
                    except Exception as e:
                        print(f"Error clicking next in form: {str(e)}")
                        failures += 1
                        pass
                    try:
                        if click_review(driver):
                            print("Successfully clicked review in form section")
                            failures = 0
                        else:
                            print("Failed to click review in form section")
                            failures += 1
                    except Exception as e:
                        print(f"Error clicking review in form: {str(e)}")
                        failures += 1
                        pass
                    time.sleep(1)

                if check_education_page(form_element=form_element) and SKIP_EDUCTATION_FORM:
                    print("ALERT: Closing job app (education form)")
                    application_error_close(driver)
                    print(f"Job application was discarded.")
                    return

                print("\n--- Processing Form Questions ---")
                # Education Element
                # Get text input questions
                text_questions = []
                print("Finding text input labels...")
                text_input_labels = [
                    q_label
                    for q_label in form_element.find_elements(By.TAG_NAME, "label")
                    if q_label.get_attribute("class") == "artdeco-text-input--label"
                ]
                text_input_labels.extend(
                    [
                        q_label
                        for q_label in form_element.find_elements(By.TAG_NAME, "label")
                        if q_label.get_attribute("data-test-single-typeahead-entity-form-title") == "true"
                    ]
                )
                print(f"Found {len(text_input_labels)} text input labels")

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

                    field_data = {"question": question, "type": field_type, "element": field}
                    print(f"Found text question: {question}")
                    text_questions.append(field_data)

                print("\n--- Processing Radio Buttons ---")
                # Get radio button input sections
                xpath_expression = '//fieldset[@data-test-form-builder-radio-button-form-component="true"]'
                radio_btn_sections = form_element.find_elements(By.XPATH, xpath_expression)
                xpath_expression = '//fieldset[@data-test-checkbox-form-component="true"]'
                checkboxes = form_element.find_elements(By.XPATH, xpath_expression)
                radio_btn_sections.extend(checkboxes)
                print(f"Found {len(radio_btn_sections)} radio/checkbox sections")

                radio_btn_questions = []
                for radio_section in radio_btn_sections:
                    section_completed = False
                    question = radio_section.find_element(By.XPATH, '//span[@aria-hidden="true"]').text
                    print(f"\nProcessing radio question: {question}")

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
                                "element": option,
                            }
                            options.append(option_info)

                    if not section_completed:
                        question_data = {
                            "question": question,
                            "type": "radio",
                            "options": options,
                            "element": options[0]["element"],
                        }
                        radio_btn_questions.append(question_data)
                        print(f"Added radio question to unanswered list: {question}")

                print("\n--- Processing Dropdown Menus ---")
                # Get dropdow menu input sections
                drop_down_questions = []
                drop_down_menus = form_element.find_elements(By.TAG_NAME, "select")
                print(f"Found {len(drop_down_menus)} dropdown menus")

                for drop_down in drop_down_menus:
                    drop_down_id = drop_down.get_attribute("id")
                    question = form_element.find_element(By.XPATH, f'//label[@for="{drop_down_id}"]').text
                    print(f"\nProcessing dropdown: {question}")

                    section_complete = False
                    options = drop_down.find_elements(By.TAG_NAME, "option")
                    options_data = []
                    for option in options:
                        if option.is_selected() and option.get_attribute("value") != "Select an option":
                            print(f"Dropdown completed (skipping): {question}")
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
                            "options": options_data,
                        }
                        drop_down_questions.append(question_data)
                        print(f"Added dropdown to unanswered list: {question}")

                print("\n--- Processing Unanswered Questions ---")
                unanswered_questions = drop_down_questions + radio_btn_questions + text_questions
                print(f"Total unanswered questions: {len(unanswered_questions)}")

                if not unanswered_questions:
                    print("No unanswered questions, proceeding to next section")
                    try:
                        if click_next(driver):
                            print("Successfully clicked next")
                            failures = 0
                        else:
                            print("Failed to click next")
                            failures += 1
                        continue
                    except Exception as e:
                        print(f"Error clicking next: {str(e)}")
                        failures += 1
                        pass
                    try:
                        if click_review(driver):
                            print("Successfully clicked review")
                            failures = 0
                        else:
                            print("Failed to click review")
                            failures += 1
                        continue
                    except Exception as e:
                        print(f"Error clicking review: {str(e)}")
                        failures += 1
                        pass

                print(f"\n- - UNANSWERED QUESTIONS - -")
                pprint(unanswered_questions)
                print(f"- - - - - - - -")

                print("\n--- Getting AI Responses ---")
                prompt = question_prompt(questions=unanswered_questions, job_description=job_description)
                response = chatgpt(prompt)
                answers = extract_json(response)
                print("AI Responses:")
                pprint(answers)

                print("\n--- Filling Form Answers ---")
                for i, question in enumerate(unanswered_questions):
                    selected_answer = answers[str(i)]
                    print(f"\nFilling answer for: {question['question']}")
                    scroll_to_element(driver, question["element"])
                    if question["type"] == "text":
                        print(f"Filling text: {selected_answer}")
                        question["element"].send_keys(selected_answer)
                    elif question["type"] == "text-numeric":
                        print(f"Filling numeric: {selected_answer}")
                        question["element"].send_keys(selected_answer)
                    elif question["type"] in ["radio", "dropdown"]:
                        print(f"Selecting option: {selected_answer}")
                        question["options"][selected_answer]["element"].click()
                    time.sleep(1)

                print("\n--- Reviewing Application ---")
                if click_next(driver):
                    print("Successfully clicked next after filling answers")
                    failures = 0
                else:
                    print("Failed to click next after filling answers")
                    failures += 1
                continue
                time.sleep(2)
            except Exception as e:
                print(f"\nERROR in form processing: {str(e)}")
                print(traceback.format_exc())
                pass

        print("\n--- Checking Review Section ---")
        if (
            get_form_section_title(driver) == "Review your application"
        ):  # and check_window(driver=driver, phrase='Review your application'):
            print("Found Review section")
            time.sleep(1)
            try:
                if click_review(driver):
                    print("Successfully clicked review")
                    failures = 0
                else:
                    print("Failed to click review")
                    failures += 1
                continue
            except Exception as e:
                print(f"Error clicking review: {str(e)}")
                failures += 1
                pass
            try:
                if click_next(driver):
                    print("Successfully clicked next")
                    failures = 0
                else:
                    print("Failed to click next")
                    failures += 1
                continue
            except Exception as e:
                print(f"Error clicking next: {str(e)}")
                failures += 1
                pass
            try:
                print("Attempting to submit application...")
                submit_application(driver)
                print("Application submitted successfully!")
                return
            except Exception as e:
                print(f"Error submitting application: {str(e)}")
                failures += 1
                pass

        print("\n--- Fallback Actions ---")
        # Fail safe, last resort
        try:
            if click_next(driver):
                print("Successfully clicked next (fallback)")
                failures = 0
            else:
                print("Failed to click next (fallback)")
                failures += 1
            continue
        except Exception as e:
            print(f"Error in fallback next: {str(e)}")
            failures += 1
            pass

        try:
            if click_review(driver):
                print("Successfully clicked review (fallback)")
                failures = 0
            else:
                print("Failed to click review (fallback)")
                failures += 1
            continue
        except Exception as e:
            print(f"Error in fallback review: {str(e)}")
            failures += 1
            pass
        # show_popup(message='Application section not recognized.\nComplete application section and press CONTINUE:')


# Pagination
def get_nav_pages(driver):
    xpath_expression = '//ul[@class="jobs-search-pagination__pages"]'
    num_elements = len(driver.find_elements(By.XPATH, xpath_expression))
    print(f"NUM ELEMENTS: {num_elements}")
    pagination_container = get_element(by=By.XPATH, selector=xpath_expression, timeout=5)
    if not pagination_container:
        print(f"WARNING: No pagination container found. (get_nav_pages)")
        return []

    scroll_to_element(driver, pagination_container)
    pages = pagination_container.find_elements(By.CSS_SELECTOR, "li.jobs-search-pagination__indicator")
    if not pages:
        print("WARNING: No pages found.")
        print(pages)
    print(f"NUM PAGES FOUND: {len(pages)}")
    return pages


def get_next_page_button(driver):
    next_page_button = driver.find_element(
        By.CSS_SELECTOR,
        "div.jobs-search-pagination.jobs-search-results-list__pagination.p4 button[aria-label='View next page']",
    )
    return next_page_button


# - - - - - - -  M A I N   E X E C U T I O N   S T A R T - - - - - - - - -
INDUSTRY = show_input_popup(
    title="Job Search Query",
    message="Enter and submit your job search query.\nE.g.: 'data scientist', 'sales executive, etc.",
)
print("")

# - - LOG IN PAGE - -
# Enter username
version_2_btn = check_sign_in_page()
if not version_2_btn:
    print(f"Sign in version 1")
    username_field = get_element(by=By.CSS_SELECTOR, selector='input[autocomplete="username"]', timeout=3)
    username_field.send_keys(USERNAME)
    time.sleep(1)

    password_field = get_element(by=By.ID, selector="session_password", timeout=3)
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

    password_field = get_element(by=By.ID, selector="password", timeout=3)
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Submit sign-in credentials
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="btn__primary--large from__button--floating"]')
    sign_in_btn.click()

# - - SECURITY CHALLENGE - -
# Wait for security challenge

# - - LINKEDIN HOMEPAGE FEED - -
# Enter search query in LinkedIn search
search_field = get_element(by=By.CSS_SELECTOR, selector='input[placeholder="Search"]', timeout=5)
if not search_field:
    show_popup(
        message="Complete security challenge if necessary and press CONTINUE.\n\n(If you are already on the LinkedIn homepage, just press CONTINUE): "
    )
    search_field = get_element(by=By.CSS_SELECTOR, selector='input[placeholder="Search"]', timeout=5)

search_field.send_keys(INDUSTRY)
search_field.send_keys(Keys.RETURN)
time.sleep(5)


# - - PEOPLE RESULTS PAGE - -
# Wait for page to load
xpath_expression = (
    ".artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--2.search-reusables__filter-pill-button"
)
get_element(by=By.CSS_SELECTOR, selector=xpath_expression, timeout=10)
# Select the 'Jobs' search filter
filter_buttons = driver.find_elements(By.CSS_SELECTOR, xpath_expression)
for button in filter_buttons:
    if "Jobs" in button.text:
        button.click()
        break

# Select the 'Easy Apply' filter
xpath_expression = '//button[@aria-label="Easy Apply filter."]'
easy_apply_filter = get_element(by=By.XPATH, selector=xpath_expression, timeout=5)
try:
    # attempt to click the easy apply filter
    easy_apply_filter.click()
except:
    # if the easy apply filter is not found, show a popup and wait for the user to press continue
    show_popup(message="Manually select the easy apply filter press CONTINUE: ")

# Manually add any additional job search filters.
show_popup(message="Manually select and apply any additional job search filters in the browser press CONTINUE:")


try:
    pages_visited = 1
    next_page = get_next_page_button(driver)

    while True:
        job_links = expose_jobs(driver)
        for link in job_links:
            scroll_to_element(driver, link)
            # time.sleep(2)
            link.click()

            xpath_expression = '//div[@id="job-details"]'
            job_description = driver.find_element(By.XPATH, xpath_expression)
            job_description = job_description.text
            print("\n- - - - JOB DESCRIPTION START - - - -")
            print(job_description)
            print("- - - - JOB DESCRIPTION END - - - -\n")
            # Click Job Application
            xpath_expression = '//button[contains(@class, "jobs-apply-button")]'
            easy_apply_button = get_element(by=By.XPATH, selector=xpath_expression, timeout=0.5)
            if not easy_apply_button:
                print("No easy apply button found. Skipping job.")
                continue

            easy_apply_button.click()
            time.sleep(1)

            try:
                print("Applying to new job.")
                easy_apply(driver, job_description)
            except Exception as e:
                print(f"Error applying to job: {str(e)}")
                print("Closinig application 2.")
                application_error_close(driver)

        # Go to next page of job search results
        next_page = get_next_page_button(driver)
        if next_page:
            pages_visited += 1
            print(f"Continuing to next page of job results. Page {pages_visited}.")
            scroll_to_element(driver, next_page)
            next_page.click()
            time.sleep(5)
        else:
            print("You have submitted all available applications for your search filter! Closing program.")
            break

except Exception as e:
    message = "An unexpected error occurred.\nPress continue to close the program. Restart the program to resume."
    # show_popup(message=message, error=True)
    # print('')
    print("- - ERROR: SOMETHING WENT WRONG - - ")
    print(traceback.format_exc())
    print("")
