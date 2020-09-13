<div align="center">
<h1>Deadline helper bot</h1>
  
[![Build Status](https://api.travis-ci.org/smirok/deadline-helper-bot.png?branch=master)](https://travis-ci.org/smirok/deadline-helper-bot)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ea0f7934d2cd4b9f8c6bf1d52108e4c0)](https://www.codacy.com/manual/smirok/Deadline-helper-bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=smirok/Deadline-helper-bot&amp;utm_campaign=Badge_Grade)
</div>

## Description
Simple telegram bot with database to control my deadlines

## Install
-   Install [Python](https://www.python.org/downloads/) latest version 
-   Clone repository: `git clone https://github.com/smirok/Deadline-helper-bot`
-   Install dependencies: `pip install -r requirements.txt`

## Run
-   Insert bot token in `cfg.py`
-   Run `python main.py`

## Commands (further settings are made via the telegram keyboard)
-   `add` - add new deadline
-   `del` - delete an existing deadline
-   `upd` - update the date of an existing deadline
-   `show` - show list of current deadlines sorted by date
