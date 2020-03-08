from django.shortcuts import render

posts = [
	{
		'author': 'Jesse',
		'title': 'Post 1',
		'content': 'Post 1 content',
		'date_posted': 'March 7, 2020'
	},
	{
		'author': 'Ryan',
		'title': 'Post 2',
		'content': 'Post 2 content',
		'date_posted': 'March 8, 2020'
	}
]


def home(request):
	context = {
		'posts': posts
	}
	return render(request, 'stats/home.html', context)

def about(request):
	return render(request, 'stats/about.html', {'title':'About'})

 

