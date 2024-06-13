# LinkedinBOT

## About 
LinkedInBOT is a tool designed to automate your job search on LinkedIn. Utilize LinkedInBOT to automate job applications and connect with recruiters in your industry.

Note: This has only been tested on Mac OS. I have not tested it on Windows.

## Features
### connect.py
1. Automated job search on LinkedIn 
2. Target recruiters by industry and / or company
3. Send custom messages to recruiters
4. Automatically personalizes messages to recruiters with their first name
### easy_apply.py
1. Automate LinkedIn Easy Apply job applications
2. Target jobs in your specific field of interest  
3. Filter job search by location / remote-friendly

## Getting Started
1. Install Google Chrome
2. Clone LinkedinBOT to your computer 
3. Create a Python virtual environment:
	- `python3 -m venv venv`
	- `source venv/bin/activate`
4. Install Dependencies:
	- `pip3 install -r requirements.txt`

## Usage: Recruiter Messaging Bot
1. Customize your message for recruiters in `introduction.txt`
	- NOTE: Be sure to leave the "FIRST_NAME" string in `introduction.txt` 
		- ( this is so the bot can address recruiter by their first name)
	- NOTE: Your introduction should not be longer than 280 characters
2. Start the bot by running `python3 connect.py`
3. Enter your LinkedIn username and password in the pop-up window if this is your first time using the bot.
4. Enter your search query (e.g. 'data science recruiter', 'Amazon recruiter', etc.) in the pop-up

## Usage: Job Application Bot 
1. Start the bot by running `python3 easy_apply.py`
2. Enter your LinkedIn username and password in the pop-up window if this is your first time using the bot.
3. Enter your desired job title in the pop-up window (e.g.: data scientist, sales executive, etc.)

## Tips
1. Create a tiny URL that links to your public resume on Google Drive or Google Docs and include the url at the bottom of your custom introduction in `introduction.txt`
2. If you accidentally entered the wrong username and password (or if you need to re-enter your username and password), simply delete the `config.json` file in the root of the project directory and re-run the bot

## Optional: Building the Standalone Desktop App (Mac OS Only)
To turn the bot into a desktop application, run the following steps:
1. Create Virtual Environment and Install Requirements
	- `python3 -m venv venv`
	- `source venv/bin/activate`
	- `pip3 install -r requirements.txt`
2. Build the Desktop App
	- `python3 setup.py py2app`

Once the application has finished building, you can find the standalone desktop application in the `/dist' directory that has been created during the build process. Since this application has not been verified by Apple you will need to open the application by right-clicking the app, and then clicking "Open."
