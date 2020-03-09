from django.shortcuts import render
from django import forms

import Game
import recap 


class GameEntry(forms.Form):

	game_id = forms.IntegerField(
		label = "Game ID",
		help_text= "Example: 401161524",
		required = True)


def home(request):
	info = {}
	if request.method == 'GET':
		form = GameEntry(request.GET)
		info['response'] = form
		if form.is_valid():
			game = Game.Game(str(form.cleaned_data['game_id']))
			info['recap_text'] = recap.generate_recap_text(game)
	info['game_form'] = form
	return render(request, 'stats/home.html', info)



 

