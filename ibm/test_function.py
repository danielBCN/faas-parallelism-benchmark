#
#
# main() will be invoked when you Run This Action.
#
# @param Cloud Functions actions accept a single parameter,
#        which must be a JSON object.
#
# @return which must be a JSON object.
#         It will be the output of this action.
#
#
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


def main(in_dict):
    init_time = time.time()
    print('Python function START')

    func_activation_ID = os.environ.get('__OW_ACTIVATION_ID')

    # Identify container
    host_name = socket.gethostname()  # This is "action" for all actions
    host_ip = socket.gethostbyname(host_name)
    # This is the docker container IP, could be repeated
    # in two different invokers.

    # Get container ID - this is the most accurate container id in docker
    command = 'head -1 /proc/self/cgroup | tr "/" "\n" | tail -1'
    container_id = os.popen(command).read().rstrip()
    command = 'cat /proc/uptime | tr " " "\n" | head -1'
    uptime = os.popen(command).read().rstrip()

    do_sleep()
    # do_work()

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
        'uptime': uptime
    }


if __name__ == "__main__":
    print(main({}))
