import bs4
import util
import re
import pandas as pd
import datetime
import requests

TEAM_NAMES_TO_CODES = {'Atlanta Hawks': 'atl',
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

TEAM_CODES_TO_NAMES = {'atl': 'Atlanta Hawks',
 'bkn': 'Brooklyn Nets',
 'bos': 'Boston Celtics',
 'cha': 'Charlotte Hornets',
 'chi': 'Chicago Bulls',
 'cle': 'Cleveland Cavaliers',
 'dal': 'Dallas Mavericks',
 'den': 'Denver Nuggets',
 'det': 'Detroit Pistons',
 'gs': 'Golden State Warriors',
 'hou': 'Houston Rockets',
 'ind': 'Indiana Pacers',
 'lac': 'LA Clippers',
 'lal': 'Los Angeles Lakers',
 'mem': 'Memphis Grizzlies',
 'mia': 'Miami Heat',
 'mil': 'Milwaukee Bucks',
 'min': 'Minnesota Timberwolves',
 'no': 'New Orleans Pelicans',
 'ny': 'New York Knicks',
 'okc': 'Oklahoma City Thunder',
 'orl': 'Orlando Magic',
 'phi': 'Philadelphia 76ers',
 'phx': 'Phoenix Suns',
 'por': 'Portland Trail Blazers',
 'sa': 'San Antonio Spurs',
 'sac': 'Sacramento Kings',
 'tor': 'Toronto Raptors',
 'uta': 'Utah Jazz',
 'wsh': 'Washington Wizards'}


def find_team_codes(names_to_codes):
    '''
    Produces dictionaries to pair official team names with ESPN team codes
    (this function generated both saved dictionaries above)
    
    Inputs:
        names_to_codes: (bool) if TRUE, map team names to team codes, if FALSE,
          map codes to names
    
    Output:
        team_codes_dict: (dict mapping str to str) a dictionary pairing team 
          codes to team names
    '''

    team_codes_dict = {}
    teams_list_request = util.read_request(
        util.get_request("https://www.espn.com/nba/teams"))
    teams_soup = bs4.BeautifulSoup(teams_list_request)
    NBA_teams = teams_soup.find_all("section", 
        class_ = "TeamLinks flex items-center")

    for team in NBA_teams:
        if names_to_codes:
            team_codes_dict[team.find("div", class_ = "pl3").find("a").\
                find("h2").text] = team.find("a")["href"][17:20].strip("/")
        else:
            team_codes_dict[team.find("a")["href"][17:20].strip("/")] = \
                team.find("div", class_ = "pl3").find("a").find("h2").text

    return team_codes_dict


def get_team_schedule(team_name, season, season_type):
    '''
    Get schedule of played games for a team in a given season for the
    preseason regular season, or postseason

    team_name: (str) the official team name of an NBA team for which to look 
      up a schedule of played games (official names found in the dictionaries 
      above)
    season: (str) a string representation of an NBA season of the format
      "2019-2020" for the season begining in the fall of 2019 and ending in
      the spring of 2020
    season_type: (str) the phase of the schedule for the team and season pair
      to return (Preseason, Regular Season, or Postseason)
    '''

    assert season_type in ("Preseason", "Regular Season", "Postseason")

    if season_type == "Preseason":
        season_type_code = "1"
    elif season_type == "Regular Season":
        season_type_code = "2"
    else:
        season_type_code = "3"
    schedule_request = util.read_request(
        util.get_request(
        "https://www.espn.com/nba/team/schedule/_/name/{}/season/{}/seasontype/{}".\
        format(TEAM_NAMES_TO_CODES[team_name], 
                  season[-4:], 
                  season_type_code)))
    schedule_soup = bs4.BeautifulSoup(schedule_request)
    schedule_table = schedule_soup.find("tbody")

    results = []
    try:
        for row in schedule_table.find_all("tr"):
            if (int(row["data-idx"]) > 0 and season_type_code != "3") \
            or int(row["data-idx"]) > 1:
                if len(row.find_all("td")) > 1:
                    if row.find_all("td")[1].find("span").text == "Opponent" \
                    and season[-4:] == str(datetime.datetime.now().year):
                        break
                    else:
                        if row.find_all("td")[0].find("span").text != "Date":
                            for cell_number, cell in enumerate(row.find_all(
                                "td")[0:3]):
                                if cell_number == 0:
                                    date = cell.find("span").text
                                elif cell_number == 1:
                                    opponent = cell.find("div").find("span", 
                                        class_ = "tc pr2").find(
                                        "a")["href"][17:20].strip("/")
                                else:
                                    game_id = cell.find("span", class_ = "ml4").\
                                    find("a")["href"][-9:]                                    

                            results.append((date, opponent, game_id))
    except:
         print("No schedule")

    return (['Date', 'Opponent', 'Game ID'], [("Invalid", "schedule selection", "for selected team")])