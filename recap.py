import Game
import pbp
import random


MADE_SHOT_SENTENCES = [
    ("In the {} quarter, {} hit a {}-point shot to make the score {}.  ",
        ["quarter", "player", "points", "score"]),
    ("{} the {} half, a {} shot for {} points swung the momentum in {}'s favor.  ",
        ["relative_time", "half", "player", "points", "player_team_city"]),
    ("A made {} point shot by {} with {} minutes left in the {} quarter went down as one of the most impactful plays on the flow of the game.  ",
        ["points", "player", "minutes", "quarter"]),
    ("{} had a timely made bucket with {} minutes to go in the {} quarter, which {} the lead to {} points.  ",
        ["name", "minutes", "quarter", "lead_increase_or_decrease", "lead"]),
    ("With {} minutes to go in the {} quarter, a shot made by {}, good for {} points, greatly helped to build momentum for his team.  ",
        ["minutes", "quarter", "player", "points"])
]

MISSED_SHOT_SENTENCES = [
    ("A fruitless {}-point attempt by {} in the {} quarter did his team no favors, causing {} to gain more momentum.  ",
        ["points", "player", "quarter", "opposing_team_nickname"]),
    ("A missed shot by {} with {} to go in the {} quarter helped to further fuel a scoring run by {}.  ",
        ["player", "minutes", "quarter", "opposing_team_city"]),
    ("With {} minutes left in the {} quarter, {}'s missed {}-point shot, led to a signifiant loss in momentum for {}.  ",
        ["minutes", "quarter", "points", "player_team_city"]),
    ("A {}-point shot attempt by {} in the {} quarter led to zero points and a significant swing in momentum in his opponents' favor.  ",
        ["points", "player", "quarter"]),
    ("Unable to hit from {} the arc, a {} shot in the {} quarter fueled a run by {}.  ",
        ["inside_or_outside", "player", "quarter", "opposing_team_city"])]

REBOUND_SENTENCES = [
    ("While perhaps unbeknownst to him at the time ({} to go in the {} quarter), {}'s succesful attempt to secure a failed shot from {} was game_altering.  ",
        ["minutes", "quarter", "player", "shooter"]),
    ("After an ill-fated shot attempt from {}, {} secured the rebound for {} and the additional momentum that went with it.  ",
        ["shooter", "player", "player_team_nickname"]),
    ("With {} to go in the {} quarter, {} tallied a rebound off a {} shot.  ",
        ["minutes", "quarter", "player", "shooter"]),
    ("A succesful rebound by {} in the {} half had significant impact on the game's flow.  ",
        ["player", "half"]),
    ("A {} rebound by {} with {} minutes and {} seconds to go in the {} quarter swung the momentum in his team's favor.  ",
        ["offensive_or_defensive", "player", "minutes", "seconds", "quarter"])
]


def generate_recap_text(game_object):

    selected_play_numbers = select_momentum_shifting_plays(game_object)

    for i in selected_plays:
        generate_text_for_a_play(i, game_object)

def select_momentum_shifting_plays(game_object):
    game_object.get_momentum_df()

    momentum_df_copy = game_object.momentum_df.copy()

    momentum_difference = []
    for row in momentum_df_copy.iterrows():
        if row[0] == 0:
            momentum_difference.append(0)
        else:
            momentum_difference.append(abs(game_object.momentum_df.iloc[row[0]].momentum -
                                           game_object.momentum_df.iloc[row[0] - 1].momentum))

    momentum_df_copy["momentum_delta"] = momentum_difference
    momentum_df_sorted = momentum_df_copy.sort_values(by = "momentum_delta", ascending = False)

    top_five_plays = momentum_df_sorted.head(5).sort_index()

    selected_play_numbers = []
    for row in top_five_plays.iterrows():
        if row[0] + 1 in selected_plays or row[0] - 1 in selected_plays:
            pass
        else:
            selected_plays_numbers.append(row[0])

    return selected_play_numbers


def generate_text_for_a_play(selected_play_number, game_object):
        selected_play = game_object.momentum_df.iloc[selected_play_numbers]
        result = None
        if "misses" in selected_play.description:
            result = "miss"
        elif "makes" in selected_play.description:
            result = "make"
        elif "rebound" in selected_play.description:
            result = "rebound"

        if result:
            if result == "miss":
                selected_sentence = random.sample(MISSED_SHOT_SENTENCES, 1)
            if result == "make":
                selected_sentence = random.sample(MADE_SHOT_SENTENCES, 1)
            if result == "rebound":
                selected_sentence = random.sample(REBOUND_SENTENCES, 1)

        list_to_paste = []
        for i in selected_sentence[1]:
            if i == "quarter":
                list_to_paste.append(str(selected_play.quarter))
            elif i == "player":
                list_to_paste.append(pbp.get_players(selected_play.description)[0])
            elif i == "points":
                if "three" in selected_play.description:
                    list_to_paste.append("3")
                if "free" in selected_play.description:
                    list_to_paste.append("1")
            elif i == "score":
                list_to_paste.append(str(selected_play.away_score) +
                                     " to "
                                     str(selected_play.home_score))
            elif i == "relative_time":
                if selected_play.quarter == 1 or selected_play.quarter == 3:
                    if selected_play.time.split(":")[0] >= 5:
                        list_to_paste.append("Early in")
                    else:
                        list_to_paste.append("Midway through")
                elif selected_play.quarter == 2 or selected_play.quarter == 4:
                    if selected_play.time.split(":") >= 5:
                        list_to_paste.append("Midway through")
                    else:
                        list_to_paste.append("Late in")
            elif i == "half":
                if selected_play.quarter == 1 or selected_play.quarter == 2:
                    list_to_paste.append("1st")
                elif selected_play.quarter == 3 or selected_play.quarter == 4:
                    list_to_paste.append("2nd")
            elif i == "player_team_city":
                if game_object.



