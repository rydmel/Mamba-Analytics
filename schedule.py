import bs4
import util
import re
import pandas as pd
import datetime
import requests

TEAM_CODES = {'Atlanta Hawks': 'atl',
 'Boston Celtics': 'bos',
 'Brooklyn Nets': 'bkn',
 'Charlotte Hornets': 'cha',
 'Chicago Bulls': 'chi',
 'Cleveland Cavaliers': 'cle',
 'Dallas Mavericks': 'dal',
 'Denver Nuggets': 'den',
 'Detroit Pistons': 'det',
 'Golden State Warriors': 'gs',
 'Houston Rockets': 'hou',
 'Indiana Pacers': 'ind',
 # The official name of the Los Angeles Clippers is in fact the "LA" Clippers
 'LA Clippers': 'lac',
 'Los Angeles Lakers': 'lal',
 'Memphis Grizzlies': 'mem',
 'Miami Heat': 'mia',
 'Milwaukee Bucks': 'mil',
 'Minnesota Timberwolves': 'min',
 'New Orleans Pelicans': 'no',
 'New York Knicks': 'ny',
 'Oklahoma City Thunder': 'okc',
 'Orlando Magic': 'orl',
 'Philadelphia 76ers': 'phi',
 'Phoenix Suns': 'phx',
 'Portland Trail Blazers': 'por',
 'Sacramento Kings': 'sac',
 'San Antonio Spurs': 'sa',
 'Toronto Raptors': 'tor',
 'Utah Jazz': 'uta',
 'Washington Wizards': 'wsh'}


def find_team_codes():
    team_codes_dict = {}
    teams_list_request = util.read_request(util.get_request("https://www.espn.com/nba/teams"))
    teams_soup = bs4.BeautifulSoup(teams_list_request)
    NBA_teams = teams_soup.find_all("section", class_ = "TeamLinks flex items-center")


    for team in NBA_teams:
        team_codes_dict[team.find("div", class_ = "pl3").find("a").find("h2").text] = \
            team.find("a")["href"][17:20].strip("/")

    return team_codes_dict


def get_team_schedule(team_name, season, season_type):
    assert season_type in ("Preseason", "Regular Season", "Postseason")
    if season_type == "Preseason":
        season_type_code = "1"
    elif season_type == "Regular Season":
        season_type_code = "2"
    else:
        season_type_code = "3"
    schedule_request = util.read_request(
        util.get_request(
        "https://www.espn.com/nba/team/schedule/_/name/{}/season/{}/seasontype/{}".format(TEAM_CODES[team_name], season[-4:], season_type_code)))
    schedule_soup = bs4.BeautifulSoup(schedule_request)
    schedule_table = schedule_soup.find("tbody")

    schedule_dates = []
    schedule_opponents = []
    schedule_game_ids = []
    for row in schedule_table.find_all("tr"):
        if (int(row["data-idx"]) > 0 and season_type_code != "3") or int(row["data-idx"]) > 1:
            if len(row.find_all("td")) > 1:
                if row.find_all("td")[1].find("span").text == "Opponent" and season[-4:] == str(datetime.datetime.now().year):
                    break
                else:
                    if row.find_all("td")[0].find("span").text != "Date":
                        for cell_number, cell in enumerate(row.find_all("td")[0:3]):
                            if cell_number == 0:
                                schedule_dates.append(cell.find("span").text)
                            elif cell_number == 1:
                                schedule_opponents.append(cell.find("div").find("span", class_ = "tc pr2").find("a")["href"][17:20].strip("/"))
                            else:
                                schedule_game_ids.append(cell.find("span", class_ = "ml4").find("a")["href"][-9:])                                        

    schedule_dataframe = pd.DataFrame(
        {"dates": schedule_dates,
         "opponent": schedule_opponents,
         "game_id": schedule_game_ids
        })

    return schedule_dataframe