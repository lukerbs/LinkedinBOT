# LinkedinBOT

## About 
LinkedInBOT is a tool for automating your job search on LinkedIn. 
To use this tool, simply define what kind of jobs you want to look for, customize your introductory message for recruiters, and run the bot. 

The bot will automatically create a new connection request and send your custom introduction to hundres of recruiters on LinkedIn that are actively hiring in your specific industry or field.

After the bot starts runnning, just kick back and wait for the recruiters to message you back with opportunities!

## Features
1. Automated job search on LinkedIn 
2. Target recruiters by industry and / or company
3. Send custom messages to recruiters
4. Automatically addresses recruiters by their first name

## Getting Started 
1. Install Google Chrome
2. Clone LinkedinBOT to your computer 
3. Create a Python virtual environment:
	- `python3 -m venv venv`
	- `source venv/bin/activate`
4. Install Dependencies:
	- `pip3 install -r requirements.txt`
6. Configure LinkedIn username and password in the `.env` file
7. Customize your message for recruiters in `introduction.txt`
	- NOTE: Be sure to leave the "FIRST_NAME" string in `introduction.txt` 
	- NOTE: Your introduction should not be longer than 280 characters
8. Start the bot by running `python3 bot.py`

## Tips
1. Create a tiny URL that links to your public resume on Google Drive or Google Docs and include the url at the bottom of your custom introduction in `introduction.txt`
