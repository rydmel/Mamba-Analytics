from django.shortcuts import render
from django import forms

import Game
import recap 
import schedule


class GameEntry(forms.Form):

	team = forms.CharField(
		label = "Full team name",
		help_text= "Example: Boston Celtics",
		required = True)

	season = forms.CharField(
		label = "Season Years",
		help_text= "Example: 2019-2020",
		required = True)

	season_phase = forms.CharField(
		label = "Season Phase",
		help_text= 'One of "Regular Season", "Preseason", "Postseason"',
		required = True)

	game_id = forms.IntegerField(
		label = "Game ID",
		help_text= "Example: 401161524",
		required = False)





def home(request):
	info = {}
	if request.method == 'GET':
		form = GameEntry(request.GET)
		info['response'] = form
		if form.is_valid():
			game = Game.Game(str(form.cleaned_data['game_id']))
			info['recap_text'] = recap.generate_recap_text(game)
			info['schedule'] = schedule.get_team_schedule(form.cleaned_data['team'], form.cleaned_data['season'], form.cleaned_data['season_phase'])
	info['game_form'] = form
	return render(request, 'stats/home.html', info)



 

