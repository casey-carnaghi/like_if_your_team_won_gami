import requests
from bs4 import BeautifulSoup


def get_nfl_scores(group_chat_teams):
    for week in range(1, 19):
        url = f"https://www.pro-football-reference.com/years/2023/week_{week}.htm"
        response = requests.get(url)
        winning_teams = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            winners = soup.find_all("tr", class_="winner")

            for winner in winners:
                team_name = winner.find('td').find('a').text
                if team_name in group_chat_teams:
                    winning_teams.append(team_name)

        print(winning_teams)


if __name__ == "__main__":
    group_chat_teams = {
        'Buffalo Bills': 'Will',
        'Detroit Lions': 'Casey',
        'Philadelphia Eagles': 'Andrew',
        'Chicago Bears': 'Sam Wood',
        'Arizona Cardinals': 'Dre',
        'New York Jets': 'Teo',
        'Green Bay Packers': 'Dylan',
        'Los Angeles Chargers': 'Stephen & Jake'
    }

    get_nfl_scores(group_chat_teams)
