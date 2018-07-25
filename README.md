# CSH Quotefault Bot
A Flask Slack bot API to interface with CSH Quotefault.

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Travis](https://travis-ci.org/mxmeinhold/csh-quotefault-bot.svg?branch=master)](https://travis-ci.org/mxmeinhold/csh-quotefault-bot)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/mxmeinhold/csh-quotefault-bot/blob/master/LICENSE)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/mxmeinhold/csh-quotefault-bot/issues)


## What's Quotefault?
[Quotefault](https://github.com/dantayy/quotefault) is a webservice to allow users to submit quotes from other members, and to allow viewing of submitted quotes.

## How's this built?
This bot is built in [Python Flask](http://flask.pocoo.org).
It handles a POST request from Slack, interprets the quote request, and responds with a quote in channel, or an ephemeral help message if the command isn't understood.
It uses the [Quotefault API](https://github.com/ComputerScienceHouse/QuotefaultAPI) to interact with the Quotefault database.

## Why build this?
I wanted to make a Slack bot, which is as simple as handling web requests.
Quotefault was a service that had an accessible API and had previously been floated as a possible Slack integration.

I made this in Flask because the last service I made was in [Node](https://nodejs.org/en/) and I wanted to get a taste of Flask.

# Contributing

Contributors welcome! Make a PR, and it will be checked with Travis and pylint. You'll need to make it pass pylint before it can be merged.

## Setup
1. Make sure you have python3 installed ([Here's a guide](https://docs.python-guide.org/starting/installation/#installation-guides))
2. You'll need pip (pip3), the python package manager ([Here's that guide](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line))
3. Run these commands to setup virtualenv and install the project dependencies to that virtualenv. This way you can have specific versions for each project without installing everything to your system.
```
python3 -m virtualenv venv # Sets up virtualenve in the venv directory in your working directory
source venv/bin/activate # Activates the virtual environment
pip install -r requirements.txt # Installs all of the dependencies listed in the requirements to the virtualenv
```
4. Set up your configuration file:
  * Copy `config.env.py` to `config.py`
  * Set `SERVER_NAME = 127.0.0.1:5000`, which is where flask will serve to. This needs to be set or else flask gets upset. You can fill in other fields if you get an api key or you're running a local mySQL DB, but they aren't strictly necessary if you aren't going to manually emulate Slack sending slash commands.
  * Set debug mode: `export FLASK_ENV=development`
  * If flask doesn't find app.py, run `export FLASK_APP=app.py`
  * Run with `flask run`
5. Make your changes, make sure it runs, and make a pull request. If you need some help with that, either checkout [GitHub's guide](https://help.github.com/articles/creating-a-pull-request/) or ping me on Slack or something.
6. Make sure your PR passes pylint, and I should merge it or message you (or comment) about any comments I have. If I don't, poke me on Slack.

If you want to check style before making a PR, you can run `pylint csh_quotefault_bot` (or `pylint -f colorized csh_quotefault_bot` for the prettier version).
