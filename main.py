from functools import reduce

import pandas as pd

# state
# player1 (position)
# player2 (position)
# rule_change (true|false)
# last_move (player1|player2)

OTHER = {
    "player1": "player2",
    "player2": "player1"
}

def perform_moves(player, state, paths):
    next_states = []
    for path in paths:
        next_box = game[state[player]][path]
        assert next_box > 0, "Illegal move"
        next_state = state.copy()
        next_state[player] = next_box
        next_state["last_move"] = player
        next_states.append(next_state)
    return next_states

def get_all_paths(player, state, game):
    paths = []
    for option in ["yes", "no", "lugnut"]:
        if game[state[player]][option] > 0:
            paths.append(option)
    return paths

def legal_paths(player, state, game):
    # ignore red texts during rule change
    if state["rule_change"] and game[state[player]]["is_red"]:
        return ["yes"]
    else:
        if game[state[player]]["look_at"] in {"this", "other"}:
            # normal rule
            player_to_look_at = player if game[state[player]]["look_at"] == "this" else OTHER[player]
            checks_to_do = game[state[player]]["check"].split(", ")
            is_yes = reduce(lambda x, y: x or y, [game[state[player_to_look_at]][check] for check in checks_to_do])
            return ["yes"] if is_yes else ["no"]
        else:
            match game[state[player]]["check"]:
                case "last_move_other":
                    return ["yes"] if state["last_move"] == OTHER[player] else ["no"]
                case "would_other_move_to_no":
                    return ["yes"] if "no" in legal_paths(OTHER[player], state, game) else ["no"]
                case "free_choice":
                    return get_all_paths(player, state, game)
                case "rule_change_on":
                    # TODO: apply rule change
                    return get_all_paths(player, state, game)
                case "move_other_to_yes":
                    # TODO: perform move other
                    return get_all_paths(player, state, game)
                case "rule_change_off":
                    # TODO: apply rule change
                    return get_all_paths(player, state, game)



            # advanced rule
            return []

def legal_next_states(state, game):
    next_states = []
    for player in ["player1", "player2"]:
        paths = legal_paths(player, state, game)
        next_states += perform_moves(player, state, paths)

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
        "player1": 55,
        "player2": 1,
        "rule_change": False,
        "last_move": "player2"
    }

    print(legal_next_states(state, game))