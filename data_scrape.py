import pandas as pd
from datetime import datetime
from functions import scrape_bundesliga_data

# Define the seasons from 2017 to current year - 1
seasons = []
start_year = 2017
end_year = datetime.now().year - 1

for year in range(start_year, end_year + 1):
    seasons.append(f"{year}-{year + 1}")

# Create the URLs
base_url = "https://fbref.com/en/comps/20/{}/schedule/{}-Bundesliga-Scores-and-Fixtures"
urls = [base_url.format(season, season) for season in seasons]

# Run the function
dataframes = [scrape_bundesliga_data(url) for url in urls]
dataframe = pd.concat(dataframes)
