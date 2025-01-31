from collections import deque
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

def perform_moves(player, state, paths, side_effect):
    next_states = []
    for path in paths:
        next_box = game[state[player]][path]
        assert next_box > 0, "Illegal move"
        next_state = state.copy()
        next_state[player] = next_box
        next_state["last_move"] = player

        # side effects
        if side_effect is not None:
            match side_effect:
                case "rule_change_on":
                    next_state["rule_change"] = True
                case "rule_change_off":
                    next_state["rule_change"] = False
                case "move_other_to_yes":
                    next_box_other = game[state[OTHER[player]]]["yes"]
                    next_state[OTHER[player]] = next_box_other
                case _:
                    assert False, "Unknown side effect"

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
        return ["yes"], None
    else:
        if game[state[player]]["look_at"] in {"this", "other"}:
            # normal rule
            player_to_look_at = player if game[state[player]]["look_at"] == "this" else OTHER[player]
            checks_to_do = game[state[player]]["check"].split(", ")
            is_yes = reduce(lambda x, y: x or y, [game[state[player_to_look_at]][check] for check in checks_to_do])
            return ["yes"] if is_yes else ["no"], None
        else:
            # advanced rule
            match game[state[player]]["check"]:
                case "last_move_other":
                    return ["yes"] if state["last_move"] == OTHER[player] else ["no"], None
                case "would_other_move_to_no":
                    return ["yes"] if "no" in legal_paths(OTHER[player], state, game) else ["no"], None
                case "free_choice":
                    return get_all_paths(player, state, game), None
                case "rule_change_on":
                    return get_all_paths(player, state, game), "rule_change_on"
                case "move_other_to_yes":
                    return get_all_paths(player, state, game), "move_other_to_yes"
                case "rule_change_off":
                    return get_all_paths(player, state, game), "rule_change_off"
                case _:
                    assert False, "Unknown check"


def legal_next_states(state, game):
    next_states = []
    for player in ["player1", "player2"]:
        paths, side_effect = legal_paths(player, state, game)
        next_states += perform_moves(player, state, paths, side_effect)

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

    # Initial state
    state = {
        "player1": 1,
        "player2": 7,
        "rule_change": False,
        "last_move": "none"
    }

    to_explore = deque([(state, [f"Player 1 at {state['player1']} and 2 at {state['player2']}"])])
    explored = set()

    while len(to_explore) > 0:
        state, path = to_explore.popleft()

        if state["player1"] == 100 or state["player2"] == 100:
            print("Found a solution:")
            for step in path:
                print(step)
            continue

        for next_state in legal_next_states(state, game):
            id = tuple(next_state.values())
            if id in explored:
                continue # avoid running in circles
            explored.add(id)

            next_path = list(path)
            next_path.append(f"Player 1 at {next_state['player1']} and 2 at {next_state['player2']}")

            to_explore.append((next_state, tuple(next_path)))


    print("Finished")
