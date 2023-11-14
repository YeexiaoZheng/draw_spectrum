import pandas as pd

def adaptive_y(max_y, step_num=4):
    max_y_str_length = len(str(max_y))
    first_digital = int(str(max_y)[0])
    if first_digital < 3:
        step = 4 * 10 ** (max_y_str_length - 2)
    elif first_digital < 5:
        step = int(0.5*10 ** (max_y_str_length - 1))
    elif first_digital < 7:
        step = int(1 * 10 ** (max_y_str_length - 1))
    elif first_digital < 9:
        step = int(1.5 * 10 ** (max_y_str_length - 1))
    else:
        step = 1 * 10 ** (max_y_str_length - 1)
    return step


def to_fomat(s: str) -> str:
    if s.lower() == 'sparkle original': return 'Sparkle'
    if s.lower() == 'sparkle partial': return 'Spectrum'
    if s.lower() == 'aria fb': return 'AriaFB'
    if s.lower() == 'serial': return 'Serial'
    return s

def add_serial(recs: pd.DataFrame, x: str, value: int):
    for _ in sorted(list(set(recs[x]))):
        if value:
            recs.loc[len(recs.index)] = { 'protocol': 'serial', x: _, 'average commit': value }
        else:
            recs.loc[len(recs.index)] = { 'protocol': 'serial', x: _, 'average commit': 28606.4 } #25301.0 } # 24398
        # recs.loc[len(recs.index)] = { 'protocol': 'serial', x: _, 'average commit': 73408.0 }

    recs.drop(index=recs[recs['threads'] == 1].index, inplace=True)
