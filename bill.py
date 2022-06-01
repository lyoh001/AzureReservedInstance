#%%
# https://docs.microsoft.com/en-us/azure/cost-management-billing/costs/manage-automation#get-usage-details-for-a-scope-during-specific-date-range
import asyncio
import calendar
import os

import aiohttp
import nest_asyncio
import pandas as pd
from IPython.display import display

nest_asyncio.apply()

df_final = pd.DataFrame()


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


async def generate_bill(session, year, month, guid):
    try:
        async with session.get(
            url=f"https://management.azure.com/subscriptions/{guid}/providers/Microsoft.Consumption/usageDetails?metric=AmortizedCost&$filter=properties/usageStart+ge+'{year}-{month:02}-01'+AND+properties/usageEnd+le+'{year}-{month:02}-{calendar.monthrange(year, month)[1]:02}'&api-version=2019-04-01-preview",
            headers=rest_api_headers,
        ) as resp:
            return pd.DataFrame(
                row["properties"] for row in (await resp.json())["value"]
            )
    except Exception:
        print(f"Error: {year}-{month}")
        return pd.DataFrame()


@timer
async def main(years, guids):
    global df_final
    async with aiohttp.ClientSession() as session:
        df_final = pd.concat(
            iter(
                await asyncio.gather(
                    *(
                        generate_bill(session, year, month, guid)
                        for guid in guids
                        for year in years
                        for month in range(1, 13)
                    )
                )
            ),
            ignore_index=True,
        )
        print(df_final.shape)


if __name__ == "__main__":
    asyncio.run(
        main(
            years=range(2019, 2023),
            guids=[os.environ["SUBSCRIPTION_IDs"]],
        )
    )
    print(list(df_final["billingPeriodStartDate"].unique()))
