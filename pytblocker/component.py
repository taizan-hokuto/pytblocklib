from typing import NamedTuple

class Component(Namedtuple):
    continuation: str
    timeout: int
    actions: list
    xsrf_token: str
    csn: str