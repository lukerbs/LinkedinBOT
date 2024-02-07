# LinkedinBOT

## About 
LinkedInBOT is a tool designed to automate your job search on LinkedIn. Utilize LinkedInBOT to automate job applications and connect with recruiters in your industry.

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
5. Configure LinkedIn username and password in the `.env` file

## Usage: Recruiter Messaging Bot
1. Customize your message for recruiters in `introduction.txt`
	- NOTE: Be sure to leave the "FIRST_NAME" string in `introduction.txt` 
	- NOTE: Your introduction should not be longer than 280 characters
2. Start the bot by running `python3 connect.py`
3. Enter your search query (e.g. 'data science recruiter', 'Amazon recruiter', etc.)

## Usage: Job Application Bot 
1. Start the bot by running `python3 easy_apply.py`
2. Enter your desired job title 


## Tips
1. Create a tiny URL that links to your public resume on Google Drive or Google Docs and include the url at the bottom of your custom introduction in `introduction.txt`

