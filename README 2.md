<!---# mobileparser [![Build Status](https://travis-ci.org/aatkin/mobileparser.png)](https://travis-ci.org/aatkin/mobileparser) # -->
# Mobileparser [![Build Status](https://drone.io/github.com/aatkin/mobileparser/status.png)](https://drone.io/github.com/aatkin/mobileparser/latest) #

## Restaurant HTML-parser for Mobilefood project ##

Crawls restaurant web pages for relevant food lists and extracts them into usable JSON-formatted data.

  * Create virtualenv folder if you haven't already: `virtualenv env` and then activate it: `source env/Scripts/activate`
  * Install requirements using pip: `pip install -r requirements.txt`
  * Run app: `python mobileparser/main.py`
  * Run tests: `nosetests` (optionally `nosetests --exe` if the test scripts are executable due to OS/editor)