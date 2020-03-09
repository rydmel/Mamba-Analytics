from pbp import * 
import util
import bs4
import re


class Game:

    def __init__(self, game_id):

        self.url = "https://www.espn.com/nba/playbyplay?gameId=" + str(game_id)
        self.game_id = game_id
        self.df = None 
        self.momentum_df = None
        self.get_game_info()
        self.get_player_set()
        self.get_revised_play_list()

    def get_game_info(self):
        self.df, self.away_team, self.away_logo, self.home_team, self.home_logo = clean_text(self.url)

    def get_momentum_df(self):
        self.momentum_df = calculate_momentum(self.df)

    def get_odds_info(self):
        odds_request = util.read_request(util.get_request("https://www.espn.com/nba/game?gameId={}".format(self.game_id)))
        odds_soup = bs4.BeautifulSoup(odds_request)

        odds_section = odds_soup.find("div", id = "gamepackage-game-information").find("div", class_ = "odds-details").find("ul")
        
        self.line = odds_section.find("li").text.strip("Line: ").lower()
        self.over_under = float(odds_section.find("li", class_ = "ou").text.strip("\n\t")[-3:])
        
    def get_player_set(self, mode = 'df'):
        if mode == 'df':
            text = list(self.df['description'])    		
        else:
            text = list(self.momentum_df['description'])
        self.players_list = get_big_player_list(text)
        player_set = set(player for l in self.players_list for player in l)
        self.player_set = player_set
        self.text = text

    def get_revised_play_list(self):
        self.revised_play_list = make_new_text_list(self.text, self.players_list)
        

    def parse_revised_text(self, s): 
        for x in l: 
            s = s.replace(x, '') 
        s = s.lstrip() 
        s = s.strip() 
        return s

    def get_player_dict(self):
        for i in range(len(self.revised_play_list)): 
            if play[0] == 'm': 
                 if 'free' not in play: 
                     parse_revised_text(play)