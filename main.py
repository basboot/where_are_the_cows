import pandas as pd

# state
# player1 (position)
# player2 (position)
# rule_change (true|false)

def perform_moves(player, state, paths):
    next_states = []
    for path in paths:
        next_box = game[state[player]][path]
        assert next_box > 0, "Illegal move"
        next_state = state.copy()
        next_state[player] = next_box
        next_states.append(next_state)
    return next_states

def legal_next_states(state, game):
    next_states = []
    for player in ["player1", "player2"]:
        # ignore red texts during rule change
        if state["rule_change"] and game[state[player]]["is_red"]:
            next_states += perform_moves(player, state, ["yes"])
        else:
            pass
    return next_states


if __name__ == '__main__':
    print("Where are the Cows?")

    # Read Excel
    df = pd.read_excel("wherearethecows.xlsx", dtype={'yes': int, 'no': int, 'lugnut': int})

    # Create game
    game = {}
    for i in range(df.shape[0]):
        box = df.iloc[i].to_dict()
        game[box["box"]] = box

    print(game)

    state = {
        "player1": 9,
        "player2": 2,
        "rule_change": True
    }

    print(legal_next_states(state, game))