import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Define function to turn time into a fractional number of hours
def time_to_frac_num(time_str):
    if not time_str: # check if the string is empty or None
        return None
    
    parts = time_str.split(":")
    if len(parts) != 2:
        return None
    
    hours, minutes = map(int, parts)
    return hours + minutes / 60.0

# Define function to pull the home and away goals
def get_home_goals(s):
    match = re.search(r"\d+", s)
    if match:
        return int(match.group())
    return None

def get_away_goals(s):
    match = re.search(r"\d+$", s)
    if match:
        return int(match.group())
    return None

# Function to scrape the data for seasons before 2017/2018
def scrape_bundesliga_data_early(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract match data
    matches = soup.select("table.stats_table tbody tr:not(.thead)")

    # Extract individual columns
    day = [match.select_one("td:nth-child(2)").get_text(strip=True) for match in matches]
    date = [match.select_one("td:nth-child(3)").get_text(strip=True) for match in matches]
    time = [match.select_one("td:nth-child(4)").get_text(strip=True) for match in matches]
    home_team = [match.select_one("td:nth-child(5)").get_text(strip=True) for match in matches]
    score = [match.select_one("td:nth-child(6)").get_text(strip=True) for match in matches]
    away_team = [match.select_one("td:nth-child(7)").get_text(strip=True) for match in matches]
    attendance = [match.select_one("td:nth-child(8)").get_text(strip=True) for match in matches]
    venue = [match.select_one("td:nth-child(9)").get_text(strip=True) for match in matches]

    match_data = pd.DataFrame({
        "date": date,
        "time": [time_to_frac_num(t) for t in time],
        "home_team": home_team,
        "score": score,
        "away_team": away_team,
        "attendance": attendance,
        "venue": venue,
        "home_goals": [get_home_goals(s) for s in score],
        "away_goals": [get_away_goals(s) for s in score]
    })

    return match_data

# Function to scrape the data
def scrape_bundesliga_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract match data
    matches = soup.select("table.stats_table tbody tr:not(.thead)")

    # Extract individual columns
    day = [match.select_one("td:nth-child(2)").get_text(strip=True) for match in matches]
    date = [match.select_one("td:nth-child(3)").get_text(strip=True) for match in matches]
    time = [match.select_one("td:nth-child(4)").get_text(strip=True) for match in matches]
    home_team = [match.select_one("td:nth-child(5)").get_text(strip=True) for match in matches]
    score = [match.select_one("td:nth-child(7)").get_text(strip=True) for match in matches]
    away_team = [match.select_one("td:nth-child(9)").get_text(strip=True) for match in matches]
    attendance = [int(match.select_one("td:nth-child(10)").get_text(strip=True).replace(',', '')) for match in matches]
    venue = [match.select_one("td:nth-child(11)").get_text(strip=True) for match in matches]

    match_data = pd.DataFrame({
        "date": pd.to_datetime(date),
        "time": [time_to_frac_num(t) for t in time],
        "home_team": home_team,
        "score": score,
        "away_team": away_team,
        "attendance": attendance,
        "venue": venue,
        "home_goals": [get_home_goals(s) for s in score],
        "away_goals": [get_away_goals(s) for s in score]
    })

    return match_data
