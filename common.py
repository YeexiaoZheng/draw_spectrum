import pandas as pd

def adaptive_y(max_y):
    max_y_str_length = len(str(max_y))
    first_digital = int(str(max_y)[0])
    if first_digital < 3:
        step = 3 * 10 ** (max_y_str_length - 2)
    elif first_digital < 6:
        step = 10 ** (max_y_str_length - 1)
    elif first_digital < 9:
        step = 2 * 10 ** (max_y_str_length - 1)
    else:
        step = 3 * 10 ** (max_y_str_length - 1)
    return step


def to_fomat(s: str) -> str:
    if s.lower() == 'sparkle original': return 'Sparkle Original'
    if s.lower() == 'sparkle partial': return 'Sparkle Partial'
    if s.lower() == 'aria fb': return 'Aria FB'
    if s.lower() == 'serial': return 'Serial'
    return s

def add_serial(recs: pd.DataFrame, x: str):
    for _ in sorted(list(set(recs[x]))):
        recs.loc[len(recs.index)] = {'protocol': 'serial', x: _, 'average commit': 94589.0}

    recs.drop(index=recs[recs['threads'] == 1].index, inplace=True)
