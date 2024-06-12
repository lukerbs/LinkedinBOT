"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


APP = ['easy_apply.py']

DATA_FILES = [
    ('assets', ['assets/success_chime.mp3', 'assets/pop.mp3', 'assets/error.mp3']), 
    'config.json',
    ('tcl8.6', ['/Library/Frameworks/Python.framework/Versions/3.10/lib/tcl8.6']),
    ('tk8.6', ['/Library/Frameworks/Python.framework/Versions/3.10/lib/tk8.6'])
]

OPTIONS = {
    'iconfile':'assets/icon.icns',
    'packages': ['tkinter'],
    'plist': {
        'CFBundleName': 'LinkedinBOT',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)