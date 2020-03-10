from django.shortcuts import render
from django import forms

import Game
import recap 
import schedule

TEAM_CHOICES = (('Atlanta Hawks', 'Atlanta Hawks'),
 ('Boston Celtics', 'Boston Celtics'),
 ('Brooklyn Nets', 'Brooklyn Nets'),
 ('Charlotte Hornets', 'Charlotte Hornets'),
 ('Chicago Bulls', 'Chicago Bulls'),
 ('Cleveland Cavaliers', 'Cleveland Cavaliers'),
 ('Dallas Mavericks', 'Dallas Mavericks'),
 ('Denver Nuggets', 'Denver Nuggets'),
 ('Detroit Pistons', 'Detroit Pistons'),
 ('Golden State Warriors', 'Golden State Warriors'),
 ('Houston Rockets', 'Houston Rockets'),
 ('Indiana Pacers', 'Indiana Pacers'),
 ('LA Clippers', 'LA Clippers'),
 ('Los Angeles Lakers', 'Los Angeles Lakers'),
 ('Memphis Grizzlies', 'Memphis Grizzlies'),
 ('Miami Heat', 'Miami Heat'),
 ('Milwaukee Bucks', 'Milwaukee Bucks'),
 ('Minnesota Timberwolves', 'Minnesota Timberwolves'),
 ('New Orleans Pelicans', 'New Orleans Pelicans'),
 ('New York Knicks', 'New York Knicks'),
 ('Oklahoma City Thunder', 'Oklahoma City Thunder'),
 ('Orlando Magic', 'Orlando Magic'),
 ('Philadelphia 76ers', 'Philadelphia 76ers'),
 ('Phoenix Suns', 'Phoenix Suns'),
 ('Portland Trail Blazers', 'Portland Trail Blazers'),
 ('Sacramento Kings', 'Sacramento Kings'),
 ('San Antonio Spurs', 'San Antonio Spurs'),
 ('Toronto Raptors', 'Toronto Raptors'),
 ('Utah Jazz', 'Utah Jazz'),
 ('Washington Wizards', 'Washington Wizards'))



YEAR_CHOICES = (("2019-2020", "2019-2020"),
	("2018-2019", "2018-2019"))

PHASE_CHOICES = (("Preseason", "Preseason"),
	("Regular Season", "Regular Season"),
	("Postseason", "Postseason"))

class ScheduleEntry(forms.Form):

	team = forms.ChoiceField(
		label = "Full team name",
		choices = TEAM_CHOICES,
		help_text= "Example: Boston Celtics",
		required = False)

	season = forms.ChoiceField(
		label = "Season Years",
		choices = YEAR_CHOICES,
		help_text= "Example: 2019-2020",
		required = False)

	season_phase = forms.ChoiceField(
		label = "Season Phase",
		choices = PHASE_CHOICES,
		help_text= 'One of "Regular Season", "Preseason", "Postseason"',
		required = False)


class GameEntry(forms.Form):
	game_id = forms.IntegerField(
		label = "Game ID",
		help_text= "Example: 401161524",
		required = False)





def home(request):
	info = {}
	if request.method == 'GET':
		form = ScheduleEntry(request.GET)
		info['response'] = form
		if form.is_valid():
			if form.cleaned_data['season_phase']:
				columns, rows = schedule.get_team_schedule(form.cleaned_data['team'], form.cleaned_data['season'], form.cleaned_data['season_phase'])
				info['columns'] = columns
				info['rows'] = rows

		form2 = GameEntry(request.GET)
		if form2.is_valid():
			if form2.cleaned_data['game_id']:
				game = Game.Game(str(form2.cleaned_data['game_id']))
				info['recap_text'] = recap.generate_recap_text(game)
				info['title_text'] = info['recap_text'][0]
				info['odds_text'] = info['recap_text'][1]
				info['plays_text'] = info['recap_text'][2]
				info['timeouts_text'] = info['recap_text'][3]

	info['schedule_form'] = form
	info['game_form2'] = form2
	return render(request, 'stats/home.html', info)



 

