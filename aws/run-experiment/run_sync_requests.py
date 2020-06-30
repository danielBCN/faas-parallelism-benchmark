import json
import time
import asyncio
import sys
import os
# import aioboto3
import aiobotocore
import botocore

config = botocore.config.Config(max_pool_connections=1000,
                                retries={'total_max_attempts': 1})

FUNCTION_NAME = "place-test"

RESULT_FILE_NAME = os.path.join("results", "{}_size={}.json")


async def async_request(client, orch_name, size):
    result_file_name = RESULT_FILE_NAME.format(orch_name, size)
    start = time.time()

    res = await client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType='RequestResponse',
        LogType='None'
    )
    query_ts = time.time()

    result = await res['Payload'].read()
    result = json.loads(result.decode())
    metadata = res['ResponseMetadata']

    start_ms = start * 1000
    end_ms = query_ts * 1000

    output = {
        # Client times:
        'pystart_ms': start_ms,
        'pyend_ms': end_ms,
        'pyduration_ms': end_ms - start_ms,

        # In-func data
        'func_data': result,
        'metadata': metadata
    }

    with open(result_file_name, 'a') as rf:
        rf.write('\n{},'.format(json.dumps(output, indent=4)))


async def main():
    session = aiobotocore.get_session()
    async with session.create_client('lambda', region_name='us-east-1',
                                     config=config) as client:
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
