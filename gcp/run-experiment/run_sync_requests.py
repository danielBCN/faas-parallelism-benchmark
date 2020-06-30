import httpx
import json
import time
import asyncio
import sys
import os

PROJECT = "bench-functions"
FUNCTION = "place-test"

HTTP_ENDPOINT_HOST = "https://us-central1-{}.cloudfunctions.net/{}"

RESULT_FILE_NAME = os.path.join("results", "{}_size={}.json")


async def async_request(client, orch_name, size):
    url = HTTP_ENDPOINT_HOST.format(PROJECT, FUNCTION)
    result_file_name = RESULT_FILE_NAME.format(orch_name, size)

    start = time.time()

    res = await client.get(url)
    query_ts = time.time()

    try:
        body = res.json()
    except Exception:
        body = res.text

    start_ms = start * 1000
    end_ms = query_ts * 1000

    output = {
        # Client times:
        'pystart_ms': start_ms,
        'pyend_ms': end_ms,
        'pyduration_ms': end_ms - start_ms,

        # In-func data
        'func_data': body
    }

    with open(result_file_name, 'a') as rf:
        rf.write('\n{},'.format(json.dumps(output, indent=4)))


async def main():
    client = httpx.AsyncClient(timeout=None,
                               pool_limits=httpx.PoolLimits(soft_limit=10,
                                                            hard_limit=1100))

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
