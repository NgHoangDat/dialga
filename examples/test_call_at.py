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
