from pbp import *



class Game:

    def __init__(self, url):

    	self.url = url
    	self.df = None 
    	self.get_momentum_df = None
    	self.get_df()
    	self.get_player_set()
    	self.get_revised_play_list()

    def get_df(self):
    	self.df = clean_text(self.url)

    def get_momentum_df(self):
    	self.momentum_df = calculate_momentum(self.df)
    	

    def get_player_set(self, mode = 'df'):
    	if mode = 'df':
    		text = list(self.df['description'])    		
    	else:
    		text = list(self.momentum_df['description'])
    	self.players_list = get_big_player_list(text)
    	player_set = set(player for l in self.players_list for player in l)
    	self.player_set = player_set
    	self.text = text

    def get_revised_play_list(self):
    	self.revised_play_list = self.make_new_text_list(self.text, self.players_list)
    	





