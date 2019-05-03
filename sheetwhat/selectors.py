from typing import Union, List, Dict

import glom

from protowhat.selectors import DispatcherInterface, T


class Dispatcher(DispatcherInterface):
    def find(self, name: str, node: T, *args, **kwargs) -> Union[List[T], Dict[str, T]]:
        # not used
        return []

    def select(self, path, node, *args, **kwargs):
        return safe_glom(node, path, *args, **kwargs)

    def parse(self, data):
        # sheetwhat-app already parses objects
        import json

        return json.loads(data)


# todo: protowhat? BoundDispatcher?
def bind_dispatcher_select(dispatcher, *data):
    def selector(path, *args, **kwargs):
        return [dispatcher.select(path, item, *args, **kwargs) for item in data]

    return selector


def dispatcher_selector(*data):
    return bind_dispatcher_select(Dispatcher(), *data)


def state_selector(state):
    return bind_dispatcher_select(
        state.dispatcher, state.student_data, state.solution_data
    )


# Supercharge path with appropriate coalesce at every level
# E.g.
#  deep_coalesce("path", None) => Coalesce("path", default=None)
#  deep_coalesce(("path", ), None) =>
#    Coalesce((Coalesce("path", default=None),), default=None)
# etc. (tuples and lists work analogously)
def deep_coalesce(path, default):
    if isinstance(path, (tuple, list)):
        path = type(path)(deep_coalesce(p, default) for p in path)
    return glom.Coalesce(path, default=default)


def safe_glom(obj, path, fallback=None):
    return glom.glom(obj, deep_coalesce(path, fallback))
