import httpx
import json
import time
import asyncio
import sys
import os
from base64 import b64encode

NAMESPACE = "some_namespace"
ACTION = "place-test"

AUTH_FILE = "userpass_auth"

HTTP_ENDPOINT_HOST = "https://us-east.functions.cloud.ibm.com"
HTTP_TRIGGER_ROUTE = "/api/v1/namespaces/{}/actions/{}"
HTTP_RQST_PARAMS = {'blocking': 'true', 'result': 'false'}

RESULT_FILE_NAME = os.path.join("results", "{}_size={}.json")


async def async_request(client, orch_name, size):
    trigger_route = HTTP_TRIGGER_ROUTE.format(NAMESPACE, ACTION)
    url = HTTP_ENDPOINT_HOST + trigger_route
    result_file_name = RESULT_FILE_NAME.format(orch_name, size)

    start = time.time()

    userAndPass = b64encode(
        bytes(open(AUTH_FILE, 'r').read(), 'utf-8')).decode("ascii")
    headers = {
        'accept': "application/json",
        'Authorization': 'Basic %s' % userAndPass,
        'content-type': "application/json"
    }

    res = await client.post(url,
                            headers=headers,
                            params=HTTP_RQST_PARAMS)
    query_ts = time.time()

    body = res.json()
    response = body.get('response')
    if response is None:
        result = body
    else:
        result = response.get('result')

    annos = body.get('annotations')
    if annos is None:
        annos = []
    wait_time = 0
    init_time = 0
    mem_lim = 0
    for a in annos:
        if a['key'] == 'waitTime':
            wait_time = a['value']
        elif a['key'] == 'initTime':
            init_time = a['value']
        elif a['key'] == 'limits':
            mem_lim = a['value']['memory']

    start_ms = start * 1000
    end_ms = query_ts * 1000

    output = {
        # Client times:
        'pystart_ms': start_ms,
        'pyend_ms': end_ms,
        'pyduration_ms': end_ms - start_ms,

        # OpenWhisk times
        'ow_func_start_ms': body.get('start'),
        'ow_func_end_ms': body.get('end'),
        'ow_func_duration_ms': body.get('duration'),

        # In-func data
        'func_data': result,

        # Extra
        'wait_time': wait_time,
        'init_time': init_time,
        'mem_lim': mem_lim
    }

    with open(result_file_name, 'a') as rf:
        rf.write('\n{},'.format(json.dumps(output, indent=4)))


async def main():
    client = httpx.AsyncClient(timeout=None,
                               pool_limits=httpx.PoolLimits(soft_limit=10,
                                                            hard_limit=1000))

    orch_name = sys.argv[1]
    num_itr = int(sys.argv[2])
    result_file_name = RESULT_FILE_NAME.format(orch_name, num_itr)
    with open(result_file_name, 'w') as rf:
        rf.write("")
    async_jobs = []
    for _ in range(num_itr):
        async_jobs.append(async_request(client, orch_name, num_itr))

    await asyncio.gather(*async_jobs)  # async

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        if not loop.is_closed():
            loop.close()
