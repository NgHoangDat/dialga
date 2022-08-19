# Dialga: call function in the future

---

> If you ever have the need to run a Python function at a specific time, or periodically. This might come handy.

```py
import asyncio
from datetime import datetime

from dialga import call_at, call_after

loop = asyncio.get_event_loop()

# This function will be call at 11:05 everyday as long that the loop is still running
@call_at(loop=loop, repeated=True, hour=11, minute=5)
def show_actual_runtime(name: str):
    print(f"Actual time of {name}:", datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S"))


# This function will be call after every 10 minutes as long as the loop is still running
@call_after(loop=loop, repeated=True, minutes=10)
def show_current_runtime(name: str):
    print(f"Current time of {name}:", datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S"))

show_actual_runtime(name="call_now")
show_current_runtime(name="call_now")

show_actual_runtime.promise(name="call_at")
show_current_runtime.promise(name="call_after")

loop.run_forever()
```

Another way to run an application:

```py
from typing import *
from datetime import datetime
from dialga import Scheduler, call_at, call_after

scheduler = Scheduler()

now = datetime.now()

@scheduler.schedule(call_at, hour=now.hour, minute=now.minute + 5)
def five_minute_from_now():
    print("Five minute from start")
    print("Start time:", datetime.strftime(now, "%y-%m-%d %H:%M:%S"))
    print("End time:", datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S"))


@scheduler.schedule(call_after, minutes=1)
def one_minute_from_now():
    print("One minute from start")
    print("Start time:", datetime.strftime(now, "%y-%m-%d %H:%M:%S"))
    print("End time:", datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S"))

scheduler.run()

```

Or another way:

- Call at:
  
```py
from datetime import datetime
from dialga import schedulable

@schedulable
def print_message(msg: str):
    now = datetime.now()
    print(now, msg)
    return now
    
print(datetime.now())
task = print_message.at(hour=17, minute=32).call('17:32')

print_message('now')
print(task.get_result())
```

- Call after:

```py
from datetime import datetime
from dialga import schedulable

@schedulable
def print_message(msg: str):
    now = datetime.now()
    print(now, msg)
    return now
    
print(datetime.now())
task = print_message.after(seconds=1).call('1 second later')

print_message('now')
print(task.get_result())
```

The `dialga` module is built upon two main function.

- `call_after`: call the function after some time

```py
def call_after(
    loop: asyncio.AbstractEventLoop = None, 
    repeated: bool = False, # Is the function called repeatly
    **timedetail # Is the parameters of datetime.timedelta
):
    ...
```

- `call_at`: call the function at specified time match the configuration

```py
def call_at(
    loop: asyncio.AbstractEventLoop = None, 
    repeated: bool = False, # Is the function called repeatly
    **timedetail # Will be explained below
):
    ...
```

`timedetail` includes these parameters: `year`, `month`, `week`, `weekday`, `day`, `hour`, `minute`, `second`, all with same format.

- None: ignore
- int: specific value
- (start, end, [step]): value in range(start, end, [step])
- [int, ...]: value in list

Note:

- a `tuple` in list is still considered as range and will be expanded.
- `week` has value from 1 -> 5
- `weekday` has value from 1 -> 7, monday -> sunday, mon -> sun, starts from monday
- `hour` has value from 0 -> 23
- `minute` and `second` hav value from 0 -> 59
- If no suitable time found, the function won't be called
