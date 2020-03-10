import Game
import pbp
import schedule
import random


TITLES = [
    ("{} beat {} by {}",
        ["winner", "loser", "lead"]),
    ("{} down {}",
        ["winner", "loser"]),
    ("{} secure the W against {} by a score of {}",
        ["winner", "loser", "score"]),
    ("{} fall to {}",
        ["loser", "winner"]),
    ("{} triumph over {} by {} points",
        ["winner", "loser", "lead"]),
    ("{} unable to stop {} in their latest battle",
        ["loser", "winner"]),
    ("ICYMI: {} no match for {}",
        ["loser", "winner"])
]


MISSED_SHOT_SENTENCES = [
    ("A fruitless {}-point attempt by {} in the {} did his team no favors, causing the {} to gain more momentum.  ",
        ["points", "player", "quarter", "opposing_team_nickname"]),
    ("A missed shot by {} with {} to go in the {} helped to further fuel a scoring run by {}.  ",
        ["player", "minutes", "quarter", "opposing_team_city"]),
    ("With {} minutes left in the {}, {}'s missed {}-point shot, led to a signifiant loss in momentum for {}.  ",
        ["minutes", "quarter", "player", "points", "player_team_city"]),
    ("A {}-point shot attempt by {} in the {} led to zero points and a significant swing in momentum in his opponents' favor.  ",
        ["points", "player", "quarter"]),
    ("Unable to hit from {} the arc, a {} shot in the {} fueled a run by {}.  ",
        ["inside_or_outside", "player", "quarter", "opposing_team_city"])]

MADE_SHOT_SENTENCES = [
    ("In the {}, {} hit a {}-point shot to make the score {}.  ",
        ["quarter", "player", "points", "score"]),
    ("{} the {}, a {} shot for {} points swung the momentum in {}'s favor.  ",
        ["relative_time", "half", "player", "points", "player_team_city"]),
    ("A made {} point shot by {} with {} minutes left in the {} went down as one of the most impactful plays on the flow of the game.  ",
        ["points", "player", "minutes", "quarter"]),
    ("{} had a timely made bucket with {} minutes to go in the {}, which {}{} points.  ",
        ["player", "minutes", "quarter", "lead_increase_or_decrease", "lead"]),
    ("With {} minutes to go in the {}, a shot made by {}, good for {} points, greatly helped to build momentum for his team.  ",
        ["minutes", "quarter", "player", "points"])
]

REBOUND_SENTENCES = [
    ("While perhaps unbeknownst to him at the time ({} to go in the {}), {}'s successful attempt to secure a failed shot from {} was game_altering.  ",
        ["minutes", "quarter", "player", "shooter"]),
    ("After an ill-fated shot attempt from {}, {} secured the rebound for the {} and the additional momentum that went with it.  ",
        ["shooter", "player", "player_team_nickname"]),
    ("With {} to go in the {}, {} tallied a rebound off a {} shot.  ",
        ["minutes", "quarter", "player", "shooter"]),
    ("A succesful rebound by {} in the {} had significant impact on the game's flow.  ",
        ["player", "half"]),
    ("{} rebound by {} with {} minutes and {} seconds to go in the {} swung the momentum in his team's favor.  ",
        ["offensive_or_defensive", "player", "minutes", "seconds", "quarter"])
]

TIMEOUTS_SENTENCES = [
    "'s head coach called timeouts when, on average, momentum was {} his team's favor.",
    "'s head coach opted to use his timeouts when momentum was {} the favor of his team, on average.",
    "'s coach was particularly inclined to call timeouts while momentum was {} his team's favor."
]

def generate_recap_text(game_object):

    selected_play_numbers = select_momentum_shifting_plays(game_object)

    title_text = generate_title_text(game_object)
    odds_text = generate_odds_text(game_object)
    plays_text = ""
    for i in selected_play_numbers:
        play_text = generate_text_for_a_play(i, game_object)
        if play_text:
            plays_text += play_text
    timeouts_text = generate_timeouts_text(game_object)
    shot_selection_text = generate_shot_selection_text(game_object)
    
    return title_text, odds_text, plays_text, timeouts_text, shot_selection_text


def generate_title_text(game_object):
    cities_or_nicknames = random.sample(["cities", "nicknames"], 1)[0]

    selected_title = random.sample(TITLES, 1)

    list_to_paste = []
    for i in selected_title[0][1]:
        if i == "winner":
            if game_object.df.tail(1).home_score.iloc[0] > game_object.df.tail(1).away_score.iloc[0]:
                if cities_or_nicknames == "cities":
                    list_to_paste.append(extract_team_city(game_object.home_team))
                else:
                    list_to_paste.append(extract_team_nickname(game_object.home_team))
            else:
                if cities_or_nicknames == "cities":
                    list_to_paste.append(extract_team_city(game_object.away_team))
                else:
                    list_to_paste.append(extract_team_nickname(game_object.away_team))
        if i == "loser":
            if game_object.df.tail(1).home_score.iloc[0] > game_object.df.tail(1).away_score.iloc[0]:
                if cities_or_nicknames == "cities":
                    list_to_paste.append(extract_team_city(game_object.away_team))
                else:
                    list_to_paste.append(extract_team_nickname(game_object.away_team))
            else:
                if cities_or_nicknames == "cities":
                    list_to_paste.append(extract_team_city(game_object.home_team))
                else:
                    list_to_paste.append(extract_team_nickname(game_object.home_team))
        if i == "lead":
            if game_object.df.tail(1).home_score.iloc[0] > game_object.df.tail(1).away_score.iloc[0]:
                list_to_paste.append(game_object.df.tail(1).home_score.iloc[0] - game_object.df.tail(1).away_score.iloc[0])
            else:
                list_to_paste.append(game_object.df.tail(1).away_score.iloc[0] - game_object.df.tail(1).home_score.iloc[0])
        if i == "score":
            if game_object.df.tail(1).home_score.iloc[0] > game_object.df.tail(1).away_score.iloc[0]:
                list_to_paste.append(str(game_object.df.tail(1).home_score.iloc[0]) + "-" + str(game_object.df.tail(1).away_score.iloc[0]))
            else:
                list_to_paste.append(str(game_object.df.tail(1).away_score.iloc[0]) + "-" + str(game_object.df.tail(1).home_score.iloc[0]))

    print(list_to_paste)
    if len(list_to_paste) == 2:
        return selected_title[0][0].format(list_to_paste[0], list_to_paste[1])
    else:
        return selected_title[0][0].format(list_to_paste[0], list_to_paste[1], list_to_paste[2])



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
        if row[0] + 1 in selected_play_numbers or row[0] - 1 in selected_play_numbers:
            pass
        else:
            selected_play_numbers.append(row[0])

    return selected_play_numbers


def generate_text_for_a_play(selected_play_number, game_object):
    selected_play = game_object.momentum_df.iloc[selected_play_number]
    result = None
    if "misses" in selected_play.description:
        result = "miss"
    elif "makes" in selected_play.description:
        result = "make"
    elif "rebound" in selected_play.description:
        result = "rebound"
    else:
        return None
    
    if result == "miss":
        selected_sentence = random.sample(MISSED_SHOT_SENTENCES, 1)
    elif result == "make":
        selected_sentence = random.sample(MADE_SHOT_SENTENCES, 1)
    elif result == "rebound":
        selected_sentence = random.sample(REBOUND_SENTENCES, 1)

    list_to_paste = []
    for i in selected_sentence[0][1]:
        if i == "quarter":
            if selected_play.quarter == 1:
                list_to_paste.append("1st quarter")
            elif selected_play.quarter == 2:
                list_to_paste.append("2nd quarter")
            elif selected_play.quarter == 3:
                list_to_paste.append("3rd quarter")
            elif selected_play.quarter == 4:
                list_to_paste.append("4th quarter")
            elif selected_play.quarter == 5:
                list_to_paste.append("1st overtime period")
            elif selected_play.quarter == 6:
                list_to_paste.append("2nd overtime period")
            elif selected_play.quarter == 7:
                list_to_paste.append("3rd overtime period")
            else:
                list_to_paste.append(str(selected_play.quarter) + "th overtime period")
        elif i == "player":
            list_to_paste.append(pbp.get_players(selected_play.description)[0])
        elif i == "points":
            if "three" in selected_play.description:
                list_to_paste.append("3")
            elif "free" in selected_play.description:
                list_to_paste.append("1")
            else:
                list_to_paste.append("2")
        elif i == "score":
            list_to_paste.append(str(selected_play.away_score) +
                                 " to " +
                                 str(selected_play.home_score))
        elif i == "relative_time":
            if selected_play.quarter == 1 or selected_play.quarter == 3:
                if int(selected_play.time.split(":")[0]) >= 5:
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
            list_to_paste.append(extract_team_city(schedule.TEAM_CODES_TO_NAMES[selected_play.team]))
        elif i == "minutes":
            time_values_list = selected_play.time.split(":")
            if (len(time_values_list[1]) > 4 & int(time_values_list[1][0]) > 2) or int(time_values_list[0]) == 0:
                list_to_paste.append(str(int(selected_play.time.split(":")[0]) + 1))
            else:
                list_to_paste.append(str(int(selected_play.time.split(":")[0])))
        elif i == "lead_increase_or_decrease":
            if selected_play.team + ".png" in game_object.home_logo:
                if selected_play.home_score > selected_play.away_score:
                    list_to_paste.append("extended the lead to ")
                elif selected_play.home_score == selected_play.away_score:
                    list_to_paste.append("tied the game at ")
                else:
                    list_to_paste.append("whittled the lead down to ")
            else:
                if selected_play.home_score < selected_play.away_score:
                    list_to_paste.append("extended the lead to ")
                elif selected_play.home_score == selected_play.away_score:
                    list_to_paste.append("tied the game at ")
                else:
                    list_to_paste.append("whittled the lead down to ")
        elif i == "lead":
            if selected_play.team + ".png" in game_object.home_logo:
                if selected_play.home_score > selected_play.away_score:
                    list_to_paste.append(str(selected_play.home_score - selected_play.away_score))
                elif selected_play.home_score == selected_play.away_score:
                    list_to_paste.append(str(selected_play.home_score))
                else:
                    list_to_paste.append(str(selected_play.away_score - selected_play.home_score))
            else:
                if selected_play.home_score < selected_play.away_score:
                    list_to_paste.append(str(selected_play.away_score - selected_play.home_score))
                elif selected_play.home_score == selected_play.away_score:
                    list_to_paste.append(selected_play.away_score)
                else:
                    list_to_paste.append(str(selected_play.home_score - selected_play.away_score))
        elif i == "opposing_team_nickname":
            if selected_play.team + ".png" in game_object.home_logo:
                list_to_paste.append(extract_team_nickname(game_object.away_team))
            else:
                list_to_paste.append(extract_team_nickname(game_object.home_team))
        elif i == "opposing_team_city":
            if selected_play.team + ".png" in game_object.home_logo:
                list_to_paste.append(extract_team_city(game_object.home_team))
            else:
                list_to_paste.append(extract_team_city(game_object.away_team))
        elif i == "inside_or_outside":
            if "three" in selected_play.description:
                list_to_paste.append("outside")
            else:
                list_to_paste.append("inside")
        elif i == "shooter":
            list_to_paste.append(pbp.get_players(game_object.momentum_df.iloc[selected_play_number - 1].description)[0])
        elif i == "player_team_nickname":
            list_to_paste.append(extract_team_nickname(schedule.TEAM_CODES_TO_NAMES[selected_play.team]))
        elif i == "offensive_or_defensive":
            if "offensive" in selected_play.description:
                list_to_paste.append("An offensive")
            else:
                list_to_paste.append("A defensive")
        elif i == "seconds":
            list_to_paste.append(selected_play.time.split(":")[1])

    print(selected_sentence)
    print(list_to_paste)
    if len(list_to_paste) == 2:
        return selected_sentence[0][0].format(list_to_paste[0], list_to_paste[1])
    elif len(list_to_paste) == 3:
        return selected_sentence[0][0].format(list_to_paste[0], list_to_paste[1], list_to_paste[2])
    elif len(list_to_paste) == 4:
        return selected_sentence[0][0].format(list_to_paste[0], list_to_paste[1], list_to_paste[2], list_to_paste[3])
    elif len(list_to_paste) == 5:
        return selected_sentence[0][0].format(list_to_paste[0], list_to_paste[1], list_to_paste[2], list_to_paste[3], list_to_paste[4])
    elif len(list_to_paste) == 6:
        return selected_sentence[0][0].format(list_to_paste[0], list_to_paste[1], list_to_paste[2], list_to_paste[3], list_to_paste[4], list_to_paste[5])


def generate_timeouts_text(game_object):
    away_timeout_avg_momentum, home_timeout_avg_momentum = determine_timeouts_momentum(game_object)

    timeouts_text = ""
    if away_timeout_avg_momentum >= 0:
        timeouts_text += extract_team_city(game_object.away_team) + random.sample(TIMEOUTS_SENTENCES, 1)[0].format("not in") + "  "
    else:
        timeouts_text += extract_team_city(game_object.away_team) + random.sample(TIMEOUTS_SENTENCES, 1)[0].format("in") + "  "
    if home_timeout_avg_momentum <= 0:
        timeouts_text += extract_team_city(game_object.home_team) + random.sample(TIMEOUTS_SENTENCES, 1)[0].format("not in")
    else:
        timeouts_text += extract_team_city(game_object.home_team) + random.sample(TIMEOUTS_SENTENCES, 1)[0].format("in")

    return timeouts_text


def determine_timeouts_momentum(game_object):

    timeouts = game_object.momentum_df[game_object.momentum_df["description"].str.find("timeout") != -1]
    away_team_timeouts_counter = 0
    away_team_cummulative_momentum = 0.0
    home_team_timeouts_counter = 0
    home_team_cummulative_momentum = 0.0
    for i in timeouts.iterrows():
        if i[1].team + ".png" in game_object.home_logo:
            home_team_timeouts_counter += 1
            home_team_cummulative_momentum += i[1].momentum
        else:
            away_team_timeouts_counter += 1
            away_team_cummulative_momentum += i[1].momentum

    if home_team_timeouts_counter == 0 and away_team_timeouts_counter == 0:
        return (0, 0)
    elif home_team_timeouts_counter == 0: 
        return (away_team_cummulative_momentum / away_team_timeouts_counter, 0)
    elif away_team_timeouts_counter == 0:
        return (0, home_team_cummulative_momentum / home_team_timeouts_counter)
    else:
        return (away_team_cummulative_momentum / away_team_timeouts_counter,
                home_team_cummulative_momentum / home_team_timeouts_counter)

def generate_odds_text(game_object):
    game_object.get_odds_info()

    if game_object.line:
        odds_text = "Spread Result: "
        spread = float(game_object.line[-5:].strip(" "))
        if "EVEN" in game_object.line:
            if game_object.df.tail(1).away_score.iloc[0] > game_object.df.tail(1).home_score.iloc[0]:
                odds_text += extract_team_nickname(game_object.home_team) + " win pick'em.  "
            else:
                odds_text += extract_team_nickname(game_object.away_team) + " win pick'em. "
        elif game_object.line[:3].strip(" ") + ".png" in game_object.home_logo:
            if game_object.df.tail(1).away_score.iloc[0] == game_object.df.tail(1).home_score.iloc[0] - spread:
                odds_text += "PUSH.  "
            elif game_object.df.tail(1).away_score.iloc[0] > game_object.df.tail(1).home_score.iloc[0] - spread:
                odds_text += extract_team_nickname(game_object.away_team) + " cover as underdogs.  "
            else:
                odds_text += extract_team_nickname(game_object.home_team) + " cover as favorites.  "
        else:
            if game_object.df.tail(1).away_score.iloc[0] - spread == game_object.df.tail(1).home_score.iloc[0]:
                odds_text += "PUSH.  "
            elif game_object.df.tail(1).away_score.iloc[0] - spread > game_object.df.tail(1).home_score.iloc[0]:
                odds_text += extract_team_nickname(game_object.away_team) + " cover as favorites.  "
            else:
                odds_text += extract_team_nickname(game_object.home_team) + " cover as underdogs.  "
      

        odds_text += "Over/Under Result: "
        if game_object.over_under == game_object.df.tail(1).away_score.iloc[0] + game_object.df.tail(1).home_score.iloc[0]:
            odds_text += "PUSH."
        elif game_object.over_under >= game_object.df.tail(1).away_score.iloc[0] + game_object.df.tail(1).home_score.iloc[0]:
            odds_text += "UNDER."
        else:
            odds_text += "OVER."
    else:
        odds_text = ""

    return odds_text


def generate_shot_selection_text(game_object):
    game_object.get_player_dict()

    selection_string = []
    for player, selections in game_object.shot_selection_dict.items():
        player_string = player + " had..."
        for types, counts in selections.items():
            player_string += str(counts) + " " + types
            if counts > 1:
                player_string += "s..."
            else:
                player_string += "..."
        selection_string.append(player_string)

    return selection_string

def extract_team_city(team_name_string):
    team_name_split = team_name_string.split(" ")
    if len(team_name_split) > 2:
        if team_name_split[0] == "Portland":
            return "Portland"
        else:
            return team_name_split[0] + " " + team_name_split[1]
    else:
        return team_name_split[0]


def extract_team_nickname(team_name_string):
    team_name_split = team_name_string.split(" ")
    if team_name_split[0] == "Portland":
        return team_name_split[1] + " " + team_name_split[2]
    else:
        return team_name_split[-1]


