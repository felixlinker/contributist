import todoist
from datetime import date
from functools import partial, reduce


def _map_delta(item):
    due = item['due']
    if not due:
        return (float('-inf'), item)
    # due date has form yyyy-mm-ddThh:mm:ss...; slice to only take into account
    # the date
    delta = date.fromisoformat(due['date'][:10]) - date.today()
    return (delta.days, item)


class TodoistConnect:
    def __init__(self, token, label_weights, default_weight):
        self.api = todoist.TodoistAPI(token)
        self.weights = label_weights
        self.default_weight = default_weight

    def connect(self):
        self.api.sync()
        weights = dict()
        for label_name, weight in self.weights.items():
            for label in self.api.state['labels']:
                if label_name == label['name']:
                    weights[label['id']] = weight
        self.weights = weights

    def _item_to_weight(self, delta_item):
        # due date has form yyyy-mm-ddThh:mm:ss; slice to only take into
        # account the date
        delta, item = delta_item
        try:
            weight = max(filter(bool, map(self.weights.get, item['labels'])))
            return (delta, weight)
        except ValueError:
            return (delta, self.default_weight)

    def _into_buckets(self, start, stop):
        start = max(0, start)
        def pred(delta_item):
            delta, _ = delta_item
            return start <= delta and delta < stop
        days = filter(pred, map(_map_delta, self.api.state['items']))

        weighted = map(self._item_to_weight, days)
        weights = [0] * (stop - start)
        for delta, weight in weighted:
            weights[delta] += weight
        return weights

    def __getitem__(self, key):
        try:
            if isinstance(key, slice):
                return self._into_buckets(key.start or 0, key.stop or float('inf'))
            elif isinstance(key, int):
                return self._into_buckets(key, key + 1)[0]
            else:
                raise TypeError()
        except StopIteration:
            raise IndexError()
