import bs4

import util

import re


def clean_text(pbp_url):
    pbp_req = util.read_request(util.get_request(pbp_url))
    pbp_soup = bs4.BeautifulSoup(pbp_req)
    pbp_tables = pbp_soup.find_all("table")

    event_times = []
    event_description = []
    event_score = []
    for pbp_table in pbp_tables:
        if pbp_table.find("tr").find("th").text == "time":
            for row in pbp_table.find_all("tr"):
                for cell in row.find_all("td"):
                    if cell['class'] == ['time-stamp']:
                        event_times.append(cell.text)
                    if cell['class'] == ['game-details']:
                        event_description.append(cell.text)
                    if cell['class'] == ['combined-score']:
                        event_score.append(cell.text)

    return event_times, event_description, event_score






def get_players(play_text):
    '''
    Input:  The text of a play (str)
    Output: list of players involved in play
    Reference: https://stackoverflow.com/questions/9525993/get-consecutive-capitalized-words-using-regex
    '''
    l = re.findall('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)', play_text)
    return l


def make_revised_play(play_text, players_list):
    for player in players_list:
        play_text = play_text.replace(player,'')
    return play_text





# Bucks vs. Thunder (game has player with periods in first name (D.J. Wilson) - rgex doesn't filter out
#game_url = 'https://www.espn.com/nba/playbyplay?gameId=401161524'



