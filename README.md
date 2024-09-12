# LinkedinBOT

## About 
LinkedInBOT is a tool designed to automate your job search on LinkedIn. LinkedInBOT leverages the OpenAI chat completions API to automatically fill out custom responses to LinkedIn Easy Apply job applications based on information in your resume. 

## Features
1. Automate LinkedIn Easy Apply job applications
2. Target jobs in your specific profession / industry / seniority level
3. Filter job search by location radius, remote, hybrid, or in-person
4. Automated and customized repsonses to job application questions with AI

## Getting Started | Installing Dependencies
1. Install Google Chrome on your desktop
2. Verify that Python is installed on your computer
2. Clone LinkedinBOT to your computer from your command line:
	- `git clone https://github.com/lukerbs/LinkedinBOT.git`
3. Enter the project directory from your command line:
	- `cd LinkedInBOT`
4. Create and activate a new Python virtual environment:
	- `python3 -m venv venv`
	- `source venv/bin/activate`
4. Install Python Dependencies:
	- `pip3 install -r requirements.txt`
5. Configure your OpenAI API Key & Environment Variable:
	- Create your OpenAI API key here if you don't have one: [Create Your OpenAI API Key](https://platform.openai.com/docs/guides/production-best-practices/api-keys)
	- Create an empty file named `.env` in the root project directory at `/LinkedinBOT/.env`
	- Copy and paste the contents `/LinkedinBOT/.env-example` into `/LinkedinBOT/.env` with your text editor
	- In the `.env` file, replace the `XXXXX` in `OPENAI_API_KEY=XXXXX` with your OpenAI API key. E.g.: `OPENAI_API_KEY=sk-hsf4ffs...`
	- Optional Step: Set the `LINKEDIN_PREMIUM` variable to `LINKEDIN_PREMIUM=true` if you have an active LinkedIn Premium subscription. Otherwise, just continue to the next step. 
	- Save the `.env` file to update your changes. 
6. Add Your Resume Details to `/LinkedinBOT/resume.txt`:
	- Open `/LinkedinBOT/resume.txt` with your text editor
	- Replace the contents of `/LinkedinBOT/resume.txt` with your resume 
	- In `/LinkedinBOT/resume.txt`, make sure to include details about your:
		- Work history and years of employment
		- Skill sets
		- Desired salary
		- Years of experience
		- Name, Location, Email, and Phone Number
		- Any other information that is likely to be asked in a job application

## Usage: Job Application Bot 
1. Start the bot by running: `python3 easy_apply.py`
2. Enter your LinkedIn username and password in the pop-up window if this is your first time using the bot.
3. Enter your desired job title in the pop-up window (e.g.: data scientist, sales executive, etc.) and click 'Continue'.
4. LinkedInBOT will log in to LinkedIn for you and search for your jobs. Wait for the next pop-up window. 
5. Optional: The bot will pause, and pop-up will appear prompting you to manually apply any job search filters. Manually select the job search filters in the browser.
	- Select your desired job filters, and make sure they are applied to the filter. 
	- Once your search filters are manually selected and applied, press 'Continue'. 
6. The bot will begin filling out custom job applications on your behalf. Now sit back and wait for the recruiters to call!

## Additional Tips
1. If you accidentally entered the wrong username and password (or if you need to re-enter your username and password), simply delete the `config.json` file in the root of the project directory and re-run the bot.
2. While the LinkedIn bot is running in your browser, make sure to keep any DMs or chat windows closed. 
3. In general, do not interfere or interact with the automated browser unless you are prompted to do so by the pop-up alert window (it may break the flow of the bot logic). However, the follow actions are usually okay to do:
	- Expanding or shrinking the automated browser window
	- Closing LinkedIn DMs that obstruct job application form fields

## Optional: Building the Standalone Desktop App (Mac OS Only)
To turn the bot into a desktop application, run the following steps:
1. Create Virtual Environment and Install Requirements
	- `python3 -m venv venv`
	- `source venv/bin/activate`
	- `pip3 install -r requirements.txt`
2. Build the Desktop App
	- `python3 setup.py py2app`

Once the application has finished building, you can find the standalone desktop application in the `/dist' directory that has been created during the build process. Since this application has not been verified by Apple you will need to open the application by right-clicking the app, and then clicking "Open."
