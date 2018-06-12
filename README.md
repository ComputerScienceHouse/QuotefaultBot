# CSH Quotefault Bot
A Flask Slack bot API to interface with CSH Quotefault.

## What's Quotefault?
[Quotefault](https://github.com/dantayy/quotefault) is a webservice to allow users to submit quotes from other members, and to allow viewing of submitted quotes.

## How's this built?
This bot is built in [Python Flask](http://flask.pocoo.org).
It handles a POST request from Slack, interprets the quote request, and responds with a quote in channel, or an ephemeral help message if the command isn't understood.
It uses the [Quotefault API](https://github.com/ComputerScienceHouse/QuotefaultAPI) to interact with the Quotefault database.

## Why build this?
I wanted to make a slack bot, which is as simple as handling web requests.
Quotefault was a service that had an accessible API and had previously been floated as a possible slack integration.

I made this in Flask because the last service I made was in [Node](https://nodejs.org/en/) and I wanted to get a taste of Flask.

# Contributing

Contributors welcome! I don't currently have any linting or formatting specifications, but preferably follow PEP 8.
