Welcome to our CMSC 12200 Project: Mamba Analytics

We have created a search engine which uses NBA play-by-play data to produce 
insights that a regular box score cannot provide.

To use our web interface, navigate to the 'testproject' directory and run the command:
"python manage.py runserver". Afterwords, open the following link in your browser: http://127.0.0.1:8000/

Our web interface allows you to first select an NBA team, an NBA season (e.g. 2019-2020), 
and a season phase which indicates the specific portion of the NBA season that you 
would like to look at. This initial query will return the schedule for your 
team of completed games information for the selected season/phase, along with the 
Game ID for each game. 

Next, you can choose a game of interest and copy the Game ID into the Game Recap 
searcher. After submitting the Game ID, a game recap is generated which summarizes
the most momentous plays determined by our momentum formula. This recap also provides
insight into whether or not each team's head coach called timeouts when momentum
was/wasn't in his team's favor. Spread and over/under results are also listed at
the top for convenient reference.

In addition, the Game Recap Search also outputs the shot selection of all the players
from the selected game by listing out the type and frequency of the shots the players took.
At the very bottom, there will be a plot of momentum throughout the game where the 
baseline of 0 indicates neutral momentum, negative momentum means momentum in the 
away team's favor, and positive momentum means momentum in the home team's favor.  
This feature is not integrated into our web app in the current version of this project
but is viewable offline using graph_momentum() in pbp.py.

As a disclaimer, we do not own the data used in this project. All data being scraped
from the web comes from ESPN.com. The image source for the header image on our 
webpage is www.clutchpoints.com.

Thanks for checking out our project!

-James, Jason, Jesse, Ryan