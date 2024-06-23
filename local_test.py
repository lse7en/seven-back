import aiohttp
import asyncio
tg_data = "query_id=AAFZ-CwEAAAAAFn4LAQpXf-S&user=%7B%22id%22%3A70056025%2C%22first_name%22%3A%22Ehsan%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22UnsortedList%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1717930112&hash=d4bb88f8fd6731dbfcc5d601d0a26109c1e05170a028f13831d0bd2d850e3707"
url = "http://localhost:4000/api/lpush"

async def make_request(session, i):
    print(str(i)*100)
    async with session.post(url) as response:
        return [i, await response.text()]


async def task(session, i):
    print(str(i)*100)
    ret = await make_request(session, i)
    print(str(i)*50)
    return ret


async def run():
    headers = {'tg-data': tg_data}
    async with aiohttp.ClientSession(headers=headers) as session:

        tasks = [asyncio.create_task(task(session, i)) for i in range(2)]
        res = asyncio.gather(*tasks)

        for i, r in await res:
            print("#"*100)
            print(i)
            print(r)


if __name__ == "__main__":


    asyncio.run(run())

36951