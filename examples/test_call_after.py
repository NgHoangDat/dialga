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
