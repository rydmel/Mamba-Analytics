import bs4
import util
import re
import pandas as pd

def clean_text(pbp_url):
    pbp_req = util.read_request(util.get_request(pbp_url))
    pbp_soup = bs4.BeautifulSoup(pbp_req)
    pbp_tables = pbp_soup.find_all("table")

    event_times = []
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
                    if cell['class'] == ['game-details']:
                        event_description.append(cell.text)
                        if cell.text == 'End of the 1st Quarter':
                            current_quarter = 2
                        if cell.text == 'End of the 2nd Quarter':
                            current_quarter = 3
                        if cell.text == 'End of the 3rd Quarter':
                            current_quarter = 4
                    if cell['class'] == ['combined-score']:
                        event_score.append(cell.text)

    pbp_dataframe = pd.DataFrame({"quarter": event_quarters,
                                  "time": event_times,
                                  "description": event_description,
                                  "score": event_score})

    pbp_dataframe[["away_score", "home_score"]] = pbp_dataframe["score"].str.split("-", expand = True).astype('int64')
    pbp_dataframe = pbp_dataframe.drop(["score"], axis = 1)
    #pbp_dataframe[["minutes, ""seconds"]] = pbp_dataframe["time"].str.split([":", "."], expand = True).astype('int64')

    return pbp_dataframe


def calculate_momentum(pbp_dataframe):
    pbp_with_momentum = pbp_dataframe.copy()
    pbp_with_momentum["momentum"] = 0.0
    pbp_dataframe["datetime"] = pd.to_datetime(pbp_dataframe["time"], format = "%M:%S.%f")
    for play in pbp_dataframe.iterrows():
        five_minutes_ago = play[1]["datetime"].minute + 5
        if five_minutes_ago > 11:
            if play[1]["quarter"] == 1:
                pbp_with_momentum["momentum"][play[0]] = determine_momentum(play[1]["away_score"], play[1]["home_score"])
            else:
                play_five_minutes_ago = pbp_dataframe[(pbp_dataframe["quarter"] == (play[1]["quarter"] - 1)) &
                                                      (pbp_dataframe["datetime"].dt.minute <= five_minutes_ago - 12) &
                                                      (pbp_dataframe["datetime"].dt.second <= play[1]["datetime"].second)].head(1)
                pbp_with_momentum["momentum"][play[0]] = determine_momentum(play[1]["away_score"] - play_five_minutes_ago["away_score"].iloc[0],
                                                                            play[1]["home_score"] - play_five_minutes_ago["home_score"].iloc[0])        
        else:
            play_five_minutes_ago = pbp_dataframe[(pbp_dataframe["quarter"] == (play[1]["quarter"])) &
                                                  (pbp_dataframe["datetime"].dt.minute <= five_minutes_ago) &
                                                  (pbp_dataframe["datetime"].dt.second <= play[1]["datetime"].second)].head(1)
            pbp_with_momentum["momentum"][play[0]] = determine_momentum(play[1]["away_score"] - play_five_minutes_ago["away_score"].iloc[0],
                                                                        play[1]["home_score"] - play_five_minutes_ago["home_score"].iloc[0])
            
    return pbp_with_momentum


def determine_momentum(away_points, home_points):
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
    #might need to consider apostrophe for players with one in their name
    l = re.findall(r"([A-Z][A-Za-z.-]+(?=\s[A-Z])(?:\s[A-Z][A-Za-z.-]+)+)", play_str)
    return l

def get_big_player_list(text_list):
    l = []
    for play in text_list:
        l.append(get_players(play))
    return l

def make_revised_play(play_text, players_list):
    for player in players_list:
        play_text = play_text.replace(player,'')
    return play_text


def make_new_text_list(play_text_list, player_list):
    action_list = []
    s = "[0-9]+[-][a-zA-Z'-]+"
    for i in range(len(play_text_list)):
        new_play = make_revised_play(play_text_list[i], player_list[i]) 
        shot_desc = re.findall(s, new_play)
        if shot_desc:
            new_play = new_play.replace(shot_desc[0], '')
        action_list.append(new_play.lstrip()) 
    return action_list



# Bucks vs. Thunder (game has player with periods in first name (D.J. Wilson) - rgex doesn't filter out
#game_url = 'https://www.espn.com/nba/playbyplay?gameId=401161524'


action_set = {'Bucks defensive team rebound',
 'Bucks offensive team rebound',
 'End of Game',
 'End of the 1st Quarter',
 'End of the 2nd Quarter',
 'End of the 3rd Quarter',
 'End of the 4th Quarter',
 'Thunder defensive team rebound',
 'Thunder delay of game violation',
 'Thunder offensive team rebound',
 'bad pass ( steals)',
 "blocks  's  driving layup",
 "blocks  's  layup",
 "blocks  's  three point jumper",
 "blocks 's driving layup",
 'defensive rebound',
 'enters the game for',
 'enters the game for ',
 'kicked ball violation',
 'loose ball foul',
 'lost ball turnover ( steals)',
 'makes  driving floating jump shot',
 'makes  driving floating jump shot ( assists)',
 'makes  dunk ( assists)',
 'makes  hook shot ( assists)',
 'makes  jumper',
 'makes  jumper ( assists)',
 'makes  pullup jump shot',
 'makes  pullup jump shot ( assists)',
 'makes  step back jumpshot',
 'makes  step back jumpshot ( assists)',
 'makes  three point jumper',
 'makes  three point jumper ( assists)',
 'makes  two point shot',
 'makes  two point shot ( assists)',
 'makes driving dunk',
 'makes driving floating jump shot',
 'makes driving layup',
 'makes driving layup ( assists)',
 'makes dunk',
 'makes dunk ( assists)',
 'makes free throw 1 of 1',
 'makes free throw 1 of 2',
 'makes free throw 1 of 3',
 'makes free throw 2 of 2',
 'makes free throw 2 of 3',
 'makes hook shot',
 'makes layup ( assists)',
 'makes pullup jump shot',
 'makes technical free throw',
 'makes tip shot',
 'makes two point shot',
 'makes two point shot ( assists)',
 'misses  hook shot',
 'misses  jumper',
 'misses  pullup jump shot',
 'misses  step back jumpshot',
 'misses  three point jumper',
 'misses  two point shot',
 'misses alley oop layup',
 'misses driving layup',
 'misses free throw 1 of 1',
 'misses free throw 1 of 2',
 'misses free throw 2 of 2',
 'misses free throw 3 of 3',
 'misses hook shot',
 'misses jumper',
 'misses pullup jump shot',
 'misses technical free throw',
 'misses three point jumper',
 'misses tip shot',
 'misses two point shot',
 'offensive charge',
 'offensive foul',
 'offensive rebound',
 'out of bounds bad pass turnover',
 'out of bounds lost ball turnover',
 'personal foul',
 'shooting foul',
 'technical foul (1st technical foul)',
 'timeout',
 'traveling',
 'turnover',
 'vs.  ( gains possession)'}

