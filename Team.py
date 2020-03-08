import schedule as sch
import Game


class Team:

    def __init__(self, name, season, season_type):
    	self.name = name
    	self.schedule = sch.get_team_schedule(name, season, season_type)
    	self.games = [Game(game_id) for game_id in self.schedule['game_id']]

    def 

    	