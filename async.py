import aiohttp
import asyncio
import matplotlib.pyplot as plt
from collections import Counter

URL = "http://localhost:5000/home"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, URL) for _ in range(10000)]
        responses = await asyncio.gather(*tasks)
    return responses

responses = asyncio.run(main())

server_counts = Counter(response['message'].split()[-1] for response in responses)

for server, count in server_counts.items():
    print(f"{server}: {count}")

servers = list(server_counts.keys())
counts = list(server_counts.values())

plt.bar(servers, counts)
plt.xlabel('Servers')
plt.ylabel('Number of Requests Handled')
plt.title('Request Distribution Among Servers')
plt.savefig('request_distribution_changed_function.png')

