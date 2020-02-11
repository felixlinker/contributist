from argparse import ArgumentParser, Action
import json
from contributist.connect import TodoistConnect

class LoadConfig(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with open(values[0], 'r') as fp:
            cfg = json.load(fp)
            for k, v in cfg.items():
                setattr(namespace, k, v)


parser = ArgumentParser()
parser.add_argument('--config', '-c', action=LoadConfig, nargs=1, required=True)
args = parser.parse_args()

connection = TodoistConnect(args.token, args.weight_tags)
connection.connect()
