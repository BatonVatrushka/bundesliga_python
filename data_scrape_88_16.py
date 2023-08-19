import pandas as pd
import requests
from bs4 import BeautifulSoup
from functions import scrape_bundesliga_data_early
import os

os.getcwd()

# Assuming scrape_bundesliga_data_early function is defined in 'functions.py'
# and has been adapted for Python
from functions import scrape_bundesliga_data_early

# Define the seasons from 1988 to 2016
seasons = [f"{year}-{year + 1}" for year in range(1988, 2017)]

# Create the URLs
base_url = "https://fbref.com/en/comps/20/{}/schedule/{}-Bundesliga-Scores-and-Fixtures"
urls = [base_url.format(season, season) for season in seasons]

# Map the function to the urls and create the df
dataframes = [scrape_bundesliga_data_early(url) for url in urls]
dataframe_early = pd.concat(dataframes)

# Save the dataframe to a CSV file
dataframe_early.to_csv('dataframe_early.csv', index=False)
