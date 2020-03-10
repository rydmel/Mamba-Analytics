from pbp import * 
import util
import bs4
import re


class Game:

    def __init__(self, game_id):
        '''
        Constructor

        Inputs:
          game_id (string): Unique ID for ESPN game (string in URL)
        '''

        self.url = "https://www.espn.com/nba/playbyplay?gameId=" + str(game_id)
        self.game_id = game_id
        self.df = None 
        self.line = None
        self.over_under = None
        self.momentum_df = None
        self.get_game_info()
        self.get_player_set()
        self.get_revised_play_list()


    def get_game_info(self):
        '''    
        Makes attributes df (Pandas DataFrame), away_team (str), home_team (str), home_logo (PNG image)    
        '''
        self.df, self.away_team, self.away_logo, self.home_team, self.home_logo = clean_text(self.url)


    def get_momentum_df(self):
        '''
        Makes attribute momentum_df (Pandas DataFrame)    
        '''
        self.momentum_df = calculate_momentum(self.df)


    def get_odds_info(self):
        '''
        Makes attributes line (str), over_under (str)    
        '''
        odds_request = util.read_request(util.get_request("https://www.espn.com/nba/game?gameId={}".format(self.game_id)))
        odds_soup = bs4.BeautifulSoup(odds_request)

        if odds_soup.find("div", id = "gamepackage-game-information").find("div", class_ = "odds-details"):

            odds_section = odds_soup.find("div", id = "gamepackage-game-information").find("div", class_ = "odds-details").find("ul")            
            self.line = odds_section.find("li").text.strip("Line: ").lower()
            self.over_under = float(odds_section.find("li", class_ = "ou").text.strip("\n\t")[-3:])
            

    def get_player_set(self, mode = 'df'):
        '''
        Default input: mode = 'df'; any other value for mode uses momentum_df
    
        Makes attributes players_list (list), player_set (set), text (list)    
        '''
        if mode == 'df':
            text = list(self.df['description'])    		
        else:
            text = list(self.momentum_df['description'])
        self.players_list = get_big_player_list(text)
        player_set = set(player for l in self.players_list for player in l)
        self.player_set = player_set
        self.text = text


    def get_revised_play_list(self):
        '''
        Makes attribute revised_play_list (list), which is a list of all the plays after players and numbers are cleaned
        '''
        self.revised_play_list = make_new_text_list(self.text, self.players_list)
        

    def parse_revised_text(self, s):
        '''    
        Helper function called in get_player_dict
        Inputs: s (str), which will be a revised play
        Output: the type of shot attempt (str)
        '''
        for x in ['makes', 'misses', '( assists)']: 
            s = s.replace(x, '') 
        s = s.lstrip() 
        s = s.strip() 
        return s


    def get_player_dict(self):
        '''
        Makes attribute shot_selection_dict (dict), which is a dict of players' types of shot attempts w/ frequency
        '''
        self.shot_selection_dict = {}
        for i in range(len(self.revised_play_list)):
            play = self.revised_play_list[i]
            if play[0] == 'm': 
                 if 'free' not in play:
                    self.shot_selection_dict[self.players_list[i][0]] = self.shot_selection_dict.get(self.players_list[i][0], {})
                    self.shot_selection_dict[self.players_list[i][0]][self.parse_revised_text(play)] = self.shot_selection_dict[self.players_list[i][0]].get(self.parse_revised_text(play), 0) + 1