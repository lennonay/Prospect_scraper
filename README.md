# Prospect Scraper

[![schedule](https://github.com/lennonay/WHL_prospect_stat/actions/workflows/schedule.yml/badge.svg)](https://github.com/lennonay/WHL_prospect_stat/actions/workflows/schedule.yml) 

Author: Lennon Au-Yeung

This project is created for the UBC Men's Hockey Analytics and Scouting team.

## About
This project aims to provide players statistics on potential recruits from the WHL for the UBC Men's Hockey team. All data collected in this project is from the official WHL and BCHL website. It automatically runs daily github action to scrape new data from the websites.

## Functions

`roster.py`: Collects birth dates and birth years of all active WHL players from every team. The purpose is to identify overage players that are currently playing in the WHL, which are our primary recruit targets.

`scraper.py`: Collects game data from the various hockey leagus, and processing into variables such as goals, primary assists and secondary assists for situations including even-strength, 5v5, powerplay and shot-handed.

`pre_processing.py`: Combines game data and roster data into a single dataframe, and transform variables to useful metrics for the scouting team such as Even Strength Goals For%(EV GF%) and Primary Points per Game.

`schedule.py`: Collects league schedule using requests, and outputs as a list of game_id to feed into `scraper.py`
