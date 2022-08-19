import asyncio
from enum import Enum
from typing import *
from typing import Callable


class State(str, Enum):
    idle: str = "idle"
    canncel: str = "cancel"
    pending: str = "pending"
    running: str = "running"
    finish: str = "finish"


class Result(NamedTuple):
    valid: bool
    data: Any


class Task:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.state: State = State.idle
        self.result = Result(False, None)
        self.schedule = None
        self.handle: Optional[asyncio.Handle] = None

    def cancel(self, *args, **kwargs):
        if self.handle:
            self.handle.cancel()
        self.state = State.canncel

    def set_state(self, state: State, *args, **kwargs):
        self.state = state

    def set_result(self, data: Any, *args, **kwargs):
        self.result = Result(True, data)

    async def wait_result(self, interval: float = 1):
        while True:
            if self.result.valid:
                break
            await asyncio.sleep(interval)

    def get_result(self, interval: float = 1):
        self.loop.run_until_complete(self.wait_result(interval))
        self.loop.close()
        return self.result.data

    async def wait(self, interval: float = 1):
        while True:
            await asyncio.sleep(interval)
            if self.state in (State.canncel, State.finish):
                break
