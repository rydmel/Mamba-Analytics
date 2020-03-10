import bs4
import util
import re
import pandas as pd
import matplotlib.pyplot as plt

def clean_text(pbp_url):
    '''
    Takes URL of an ESPN NBA play-by-play page and creates an
    organized dataframe with play descriptions, time, and score

    Input: pbp_url- a URL string
    Returns: 
        pbp_dataframe- Pandas dataframe
        away_logo- PNG image of away team's logo
        away_team- name of away team
        home_team- name of home team
        home_logo- PNG image of home team's logo

    '''

    pbp_req = util.read_request(util.get_request(pbp_url))
    pbp_soup = bs4.BeautifulSoup(pbp_req)


    pbp_soup = bs4.BeautifulSoup(pbp_req)
    away_team, away_logo = find_team_name_and_logo(pbp_soup, False)
    home_team, home_logo = find_team_name_and_logo(pbp_soup, True)

    pbp_tables = pbp_soup.find_all("table")

    event_times = []
    event_team = []
    event_description = []
    event_score = []
    event_quarters = []
    current_quarter = 1
    for pbp_table in pbp_tables:
        if pbp_table.find("tr").find("th").text == "time":
            for row in pbp_table.find_all("tr"):
                for cell in row.find_all("td"):
                    if cell['class'] == ['time-stamp']:
                        if "." in cell.text:
                            event_times.append("0:" + cell.text)
                        else:
                            event_times.append(cell.text + ".00")

                        event_quarters.append(current_quarter)
                    if cell['class'] == ['logo']:
                        event_team.append(cell.find("img")['src'][58:61].\
                            strip("."))
                    if cell['class'] == ['game-details']:
                        event_description.append(cell.text)
                        if 'End of the' in cell.text:
                                current_quarter += 1
                    if cell['class'] == ['combined-score']:
                        event_score.append(cell.text)

    pbp_dataframe = pd.DataFrame({"quarter": event_quarters,
                                  "time": event_times,
                                  "team": event_team,
                                  "description": event_description,
                                  "score": event_score})

    pbp_dataframe[["away_score", "home_score"]] = pbp_dataframe["score"].str.\
    split("-", expand = True).astype('int64')
    pbp_dataframe = pbp_dataframe.drop(["score"], axis = 1)

    return pbp_dataframe, away_team, away_logo, home_team, home_logo


def find_team_name_and_logo(pbp_soup, is_home):
    '''
    Takes BeautifulSoup object and extracts team name

    Inputs: 
        pbp_soup- BeautifulSoup object
        is_home- Boolean indicating whether name of desired team is home or away

    Returns:
        team_name- team name in string form
    '''

    if is_home:
        if pbp_soup.find("div", class_ = "competitors sm score"):
            team_location = pbp_soup.find("div", 
                class_ = "competitors sm-score").find("div", 
                class_ = "team home")
        else:
            team_location = pbp_soup.find("div", class_ = "competitors").\
            find("div", class_ = "team home")
        
    else:
        if pbp_soup.find("div", class_ = "competitors sm score"):
            team_location = pbp_soup.find("div", class_ = "competitors sm-score").\
            find("div", class_ = "team away")
        else:
            team_location = pbp_soup.find("div", class_ = "competitors").\
            find("div", class_ = "team away")
        
    return team_location.find("span", class_ = "long-name").text + ' ' + team_location.find("span", class_ = "short-name").text, team_location.find("img", class_ = "team-logo")["src"]


def calculate_momentum(pbp_dataframe):
    '''
    Calculates a momentum stat for each play

    Inputs: pbp_dataframe- Pandas dataframe returned from clean_text

    Returns: pbp_with_momentum- Dataframe with momentum column appended
    '''
    
    pbp_with_momentum = pbp_dataframe[:-1].copy()
    momentum_list = []
    pbp_dataframe["datetime"] = pd.to_datetime(pbp_dataframe["time"], 
        format = "%M:%S.%f")
    for play in pbp_dataframe.iterrows():
        is_overtime = False
        if play[1]["quarter"] >= 5:
            is_overtime = True
        # Momentum is a function of the points scored by each team over the
        # previous five minutes of gameplay
        five_minutes_ago = play[1]["datetime"].minute + 5
        if is_overtime:
            play_five_minutes_ago = pbp_dataframe[(pbp_dataframe["quarter"] == \
                (play[1]["quarter"] - 1)) &
                (pbp_dataframe["datetime"].dt.minute <= five_minutes_ago - 5) &
                (pbp_dataframe["datetime"].dt.second <= play[1]["datetime"].\
                    second)].head(1)
            momentum_list.append(determine_momentum(play[1]["away_score"] - \
                play_five_minutes_ago["away_score"].iloc[0],
                play[1]["home_score"] - play_five_minutes_ago["home_score"].\
                iloc[0]))
        else:
            if five_minutes_ago >= 12:
                if play[1]["quarter"] == 1:
                    momentum_list.append(0.0)
                else:
                    play_five_minutes_ago = pbp_dataframe[(pbp_dataframe\
                        ["quarter"] == (play[1]["quarter"] - 1)) &
                        (pbp_dataframe["datetime"].dt.minute <= \
                            five_minutes_ago - 12) &
                        (pbp_dataframe["datetime"].dt.second <= \
                            play[1]["datetime"].second)].head(1)
                    momentum_list.append(determine_momentum(play[1]\
                        ["away_score"] - play_five_minutes_ago["away_score"].\
                        iloc[0],
                        play[1]["home_score"] - play_five_minutes_ago\
                        ["home_score"].iloc[0]))     
            else:
                play_five_minutes_ago = pbp_dataframe[(pbp_dataframe\
                    ["quarter"] == (play[1]["quarter"])) &
                    (pbp_dataframe["datetime"].dt.minute <= five_minutes_ago) &
                    (pbp_dataframe["datetime"].dt.second <= play[1]["datetime"]\
                        .second)].head(1)
                momentum_list.append(determine_momentum(play[1]["away_score"] -\
                play_five_minutes_ago["away_score"].iloc[0],
                play[1]["home_score"] - play_five_minutes_ago["home_score"].\
                iloc[0]))
    
    pbp_with_momentum["momentum"] = momentum_list[:len(momentum_list) - 1] 

    return pbp_with_momentum


def graph_momentum(pbp_with_momentum):
    '''
    Plots momentum on a graph for easy visualization
        -Negative values favor the away team
        -Positive values favor the home team

    Inputs: pbp_with_momentum- Dataframe with momentum column appended
    '''

    plt.plot(pbp_with_momentum["momentum"], color = "orange", 
        label = "Momentum")
    plt.plot(range(0,len(pbp_with_momentum)), [0]*len(pbp_with_momentum), 
        color = "gray", 
        label = "Neutral", 
        linestyle = "--")
    plt.title("NBA momentum by play-by-play event sequence")
    plt.xlabel("Play-by-play event number")
    plt.ylabel("Momentum")
    plt.ylim(-14, 14)
    plt.legend()
    plt.show()


def determine_momentum(away_points, home_points):
    '''
    Formula for calculating momentum level at a given play

    Inputs:
        away_points- integer representing away team's points
        home_points- integer representing home team's points

    Returns:
        momentum- floating point number representing momentum level
    '''

    if away_points > home_points:
        return -1 * float((away_points + 1) / (home_points + 1))
    else:
        return float((home_points + 1) / (away_points + 1))
  

def get_players(play_str):
    '''
    Input:  The text of a play (str)
    Output: list of players involved in play
    Reference: https://stackoverflow.com/questions/9525993/get-consecutive-capitalized-words-using-regex
    '''

    l = re.findall(r"([A-Z][A-Za-z.\'-]+(?=\s[A-Z])(?:\s[A-Z][A-Za-z.\'-]+)+)", 
        play_str)
    
    return l


def get_big_player_list(text_list):
    '''
    Returns all players involved from a list of plays

    Inputs: text_list- list of plays
    Returns: l- list of players
    '''
    
    l = []
    for play in text_list:
        l.append(get_players(play))
    return l


def make_revised_play(play_text, players_list):
    '''
    Inputs: play_text (str), players_list (list)
    Returns: string without players 
    '''
    
    for player in players_list:
        play_text = play_text.replace(player,'')
    return play_text


def make_new_text_list(play_text_list, player_list):
    '''
    Inputs: play_text_list (list), players_list (list)
    Returns: list of strings, which are the actions in each play
    '''

    action_list = []
    s = "[0-9]+[-][a-zA-Z'-]+"
    for i in range(len(play_text_list)):
        new_play = make_revised_play(play_text_list[i], player_list[i]) 
        shot_desc = re.findall(s, new_play)
        if shot_desc:
            new_play = new_play.replace(shot_desc[0], '')
        action_list.append(new_play.lstrip()) 
    return action_list


def calculate_points_off_timeout(play_text_list):
    '''
    Inputs: play_text_list (df)
    Returns: count (int) - number of total points scored off turnovers for both teams combined
    '''

    count = 0
    reverse = play_text_list.iloc[::-1]
    flag = 0
    for index, row in reverse.iterrows():
        if flag == 2:
    	    if 'makes' in row['description'] and 'free throw' in \
            row['description']:
    	        count += 1
    	    else:
    	        flag = 0
        if 'timeout' in row['description']:
            flag = 1
        elif 'makes' in row['description'] and flag:
            if 'free throw' in row['description']:
                count += 1
                flag = 2
            elif 'three point' in row['description']:
                count += 3
                flag = 0
            else:
                count += 2
                flag = 0
        elif 'defensive' in row['description'] and 'rebound' in \
        row['description'] and flag:
            flag = 0
        elif 'turnover' in row['description'] and flag:
            flag = 0
    
    return count
