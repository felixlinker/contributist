import todoist
from datetime import date
from functools import partial


def _filter_due(lower, upper, item):
    due = item['due']
    if not due:
        return False
    # due date has form yyyy-mm-ddThh:mm:ss...; slice to only take into account
    # the date
    delta = date.fromisoformat(due['date'][:10]) - date.today()
    return lower <= delta.days and delta.days <= upper


class TodoistConnect:
    def __init__(self, token, label_weights):
        self.api = todoist.TodoistAPI(token)
        self.weights = label_weights

    def connect(self):
        self.api.sync()
        weights = dict()
        for label_name, weight in self.weights.items():
            for label in self.api.state['labels']:
                if label_name == label['name']:
                    weights[label['id']] = weight
        self.weights = weights

    def _map_label(self, label_id):
        return self.weights.get(label_id, None)

    def __getitem__(self, key):
        try:
            if isinstance(key, slice):
                start = key.start or float('-inf')
                stop = key.stop or float('inf')
                return list(filter(partial(_filter_due, start, stop), self.api.state['items']))
            elif isinstance(key, int):
                return next(filter(partial(_filter_due, key, key), self.api.state['items']))
            else:
                raise TypeError()
        except StopIteration:
            raise IndexError()
