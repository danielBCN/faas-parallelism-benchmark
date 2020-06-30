import socket
import os
import time


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


def handler(event, context):
    init_time = time.time()
    print('Python function START')

    if context is not None:
        func_activation_ID = context.aws_request_id
        func_mem_limit = context.memory_limit_in_mb

    # Identify container
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    command = 'cat /proc/self/cgroup | grep sandbox-root'
    container_id = os.popen(command).read().rstrip()
    command = 'cat /proc/uptime | tr " " "\n" | head -1'
    uptime = os.popen(command).read().rstrip()

    # do_sleep()
    do_work()

    print('Python function END')
    end_time = time.time()

    return {
        'initTime_ms': init_time*1000,
        'endTime_ms': end_time*1000,
        'duration_ms': (end_time-init_time)*1000,
        'funcActivationID': func_activation_ID,
        'hostname': host_name,
        'hostnameIP': host_ip,
        'containerID': container_id,
        'mem_limit': func_mem_limit,
        'uptime': uptime,
    }


if __name__ == "__main__":
    print(handler({}, None))
