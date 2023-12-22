import requests
from bs4 import BeautifulSoup
import time
import sys
import pandas as pd


def get_nfl_scores(group_chat_teams, data_file, year):
    df = pd.read_csv(data_file, index_col=0)

    if year >= 2021:
        last_week = 23
    else:
        last_week = 22

    for week in range(1, last_week):
        url = f"https://www.pro-football-reference.com/years/{year}/week_{week}.htm"
        response = requests.get(url)
        winning_teams = []

        print(f"{year} Week {week} winners:\n")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            winners = soup.find_all("tr", class_="winner")

            for winner in winners:
                team_name = winner.find('td').find('a').text

                if team_name in group_chat_teams:
                    winning_teams.append(team_name)

        else:
            print(f"Could not access {url}. Reponse: {response}")
            sys.exit()

        winning_teams = '\n'.join(winning_teams)

        df.at[f"Week {week}", f"{year}"] = winning_teams
        df.to_csv(data_file)

        print(winning_teams)
        print('***********************\n')

        # sleep for 3 seconds to abide by sportsreferences
        # guidelines of no more than 20 request per minute
        time.sleep(3)


def create_csv(data_file):
    df = pd.DataFrame()
    start_year = 1997
    end_year = 2023
    weeks = list(range(1, 22))

    # add column for each year
    for year in range(start_year, end_year + 1):
        year_column = f'{year}'
        df[year_column] = None

    # add rows for each week
    for week in weeks:
        df.loc[f'Week {week}'] = None

    df.to_csv(data_file, index=True)


if __name__ == "__main__":
    data_file = 'data.csv'
    create_csv(data_file)

    group_chat_teams = {
        'Buffalo Bills': 'Will',
        'Detroit Lions': 'Casey',
        'Philadelphia Eagles': 'Andrew',
        'Chicago Bears': 'Sam Wood',
        'Arizona Cardinals': 'Dre',
        'New York Jets': 'Teo',
        'Green Bay Packers': 'Dylan',
        'Los Angeles Chargers': 'Stephen & Jake',
        'San Diego Chargers': 'Jake & Stephen'
    }

    check = False
    year = 1997
    while check is not True:
        if year == 2024:
            check = True
            break

        get_nfl_scores(group_chat_teams, data_file, year)
        year += 1
