# cricket_scores.py

def batting_points(player):
    """Calculate total points for a batting player."""
    points = 0
    runs = player['runs']
    balls = player['balls']
    fours = player['4']
    sixes = player['6']

    # Runs points: 1 point per 2 runs
    points += runs // 2

    # Milestone bonuses
    if runs >= 100:
        points += 10
        points += 5
    elif runs >= 50:
        points += 5

    # Strike rate bonus
    strike_rate = (runs / balls) * 100

    if strike_rate > 100:
        points += 6
    elif 80 <= strike_rate <= 100:
        points += 2

    # Boundary points
    points += fours
    points += sixes * 2

    # Fielding points
    points += player['field'] * 10

    return points


def bowling_points(player):
    """Calculate total points for a bowling player."""
    points = 0

    wickets = player['wkts']
    overs = player['overs']
    runs = player['runs']

    # Wicket points
    points += wickets * 10

    # Wicket milestone bonuses
    if wickets >= 5:
        points += 15
    elif wickets >= 3:
        points += 5

    # Economy rate bonus
    economy = runs / overs

    if economy < 2:
        points += 10
    elif 2 <= economy < 3.5:
        points += 7
    elif 3.5 <= economy <= 4.5:
        points += 4

    # Fielding points
    points += player['field'] * 10

    return points