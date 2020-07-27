from argparse import ArgumentParser, Action
import json
import numpy as np
from datetime import date
from math import ceil

from contributist.connect import TodoistConnect
from contributist.viz import plt_heatmap

class LoadConfig(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open(values[0], 'r', encoding='utf-8') as fp:
            cfg = json.load(fp)
            for k, v in cfg.items():
                setattr(namespace, k, v)


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

parser = ArgumentParser()
parser.add_argument('--config', '-c', action=LoadConfig, nargs=1, required=True)
parser.add_argument('--days', '-d', type=int, nargs='?', default=28)
args = parser.parse_args()

connection = TodoistConnect(args.token, args.weight_tags, args.default_weight)
connection.connect()

weights = connection[:args.days]
today = date.today()
weekday = today.weekday()
_, isoweek, _ = today.isocalendar()
weeks = list(range(ceil((args.days + weekday) / len(WEEKDAYS))))


def week_slice(week):
    start = week * len(WEEKDAYS) - weekday
    return slice(max(0, start), start + 7)


heat_matrix = [weights[week_slice(week)] for week in weeks]
# Front-pad missing days as zero for first week
heat_matrix[0] = [0] * weekday + heat_matrix[0]
# Tail-pad missing days as zero for last week
heat_matrix[-1] = heat_matrix[-1] + [0] * \
    max(0, len(WEEKDAYS) - len(heat_matrix[-1]))

plt_heatmap(np.array(heat_matrix),
            list(map(lambda d: d[:2], WEEKDAYS)),       # only show first two letters
            list(map(lambda w: w + isoweek, weeks)))    # display week number on y axis
