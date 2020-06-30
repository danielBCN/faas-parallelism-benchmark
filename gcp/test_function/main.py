# import socket
import os
import time
import json
import uuid


container_id = str(uuid.uuid4())


def do_sleep():
    time.sleep(1)


def do_work():
    from random import random
    iterations = 5_000_000

    count = 0
    for _ in range(iterations):
        x = random()
        y = random()
        if x*x + y*y <= 1.0:
            count = count + 1
    pi = 4.0 * count / iterations
    print(pi)


def main(request):
    init_time = time.time()
    print('Python function START')

    execution_id = request.headers.get("Function-Execution-Id")

    # do_sleep()
    do_work()

    print('Python function END')
    end_time = time.time()

    return json.dumps({
        'initTime_ms': init_time*1000,
        'endTime_ms': end_time*1000,
        'duration_ms': (end_time-init_time)*1000,
        'executionID': execution_id,
        'containerID': container_id,
    }, indent=2)


if __name__ == "__main__":
    print(main({}))
