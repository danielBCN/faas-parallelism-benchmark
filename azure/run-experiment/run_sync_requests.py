import httpx
import json
import time
import asyncio
import sys
import os

SLEEP_TIME = 5000
HTTP_TRIGGER_URL = "https://func-place.azurewebsites.net/api/BenchFunc"
RESULT_FILE_NAME = os.path.join("results", "{}_size={}.json")


async def async_request(client, orch_name, size):
    trigger_url = HTTP_TRIGGER_URL
    result_file_name = RESULT_FILE_NAME.format(orch_name, size)

    start = time.time()

    res = await client.get(trigger_url)
    query_ts = time.time()

    body = json.loads(res.text)

    start_ms = start * 1000
    end_ms = query_ts * 1000

    func_start = body['Init']
    func_end = body['End']
    func_invocationId = body['InvocationID']
    func_instanceId = body['InstanceID']

    output = {}
    output['pystart_ms'] = start_ms
    output['pyend_ms'] = end_ms
    output['pyduration_ms'] = end_ms - start_ms

    output['start'] = func_start
    output['end'] = func_end
    output['duration'] = func_end - func_start
    output['invocation'] = func_invocationId
    output['instance'] = func_instanceId

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
        loop.close()
