#%%
import asyncio
import base64
import functools
import os
import time

import aiohttp
import nest_asyncio

nest_asyncio.apply()


(
    graph_api_headers,
    rest_api_headers,
    devops_api_headers,
    devops_pat_headers,
    ea_api_headers,
) = [""] * 5


def timer(func):
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            await func(*args, **kwargs)
            print(f"total runtime for async func: {time.time() - start_time}")

        return wrapper
    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            print(f"total runtime for sync func: {time.time() - start_time}")

        return wrapper


def get_api_headers_decorator(func):
    @functools.wraps(func)
    async def wrapper(session, *args, **kwargs):
        return {
            "Authorization": f"Basic {base64.b64encode(bytes(os.environ[args[0]], 'utf-8')).decode('utf-8')}"
            if "PAT" in args[0]
            else f"Bearer {os.environ[args[0]] if 'EA' in args[0] else await func(session, *args, **kwargs)}",
            "Content-Type": "application/json-patch+json"
            if "PAT" in args[0]
            else "application/json",
        }

    return wrapper


@get_api_headers_decorator
async def get_api_headers(session, *args, **kwargs):
    oauth2_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    oauth2_body = {
        "client_id": os.environ[args[0]],
        "client_secret": os.environ[args[1]],
        "grant_type": "client_credentials",
        "scope" if "GRAPH" in args[0] else "resource": args[2],
    }
    async with session.post(
        url=args[3], headers=oauth2_headers, data=oauth2_body
    ) as resp:
        return (await resp.json())["access_token"]


@timer
async def main(params):
    global graph_api_headers, rest_api_headers, devops_api_headers, devops_pat_headers, ea_api_headers
    async with aiohttp.ClientSession() as session:
        (
            graph_api_headers,
            rest_api_headers,
            devops_api_headers,
            devops_pat_headers,
            ea_api_headers,
        ) = await asyncio.gather(
            *(get_api_headers(session, *param) for param in params)
        )


if __name__ == "__main__":
    params = [
        [
            "GRAPH_CLIENT_ID",
            "GRAPH_CLIENT_SECRET",
            "https://graph.microsoft.com/.default",
            f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}/oauth2/v2.0/token",
        ],
        [
            "REST_CLIENT_ID",
            "REST_CLIENT_SECRET",
            "https://management.azure.com",
            f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}/oauth2/token",
        ],
        [
            "DEVOPS_CLIENT_ID",
            "DEVOPS_CLIENT_SECRET",
            "https://management.azure.com",
            f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}/oauth2/token",
        ],
        ["DEVOPS_PAT_TOKEN"],
        ["PRIMARY_EA_API_TOKEN"],
    ]
    asyncio.run(main(params))
