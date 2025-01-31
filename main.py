import pandas as pd

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
