import asyncio
import aiohttp
import matplotlib.pyplot as plt

async def measure_server_load(num_servers):
    url = 'http://localhost:5000/home'
    server_loads = {f"server{i+1}": 0 for i in range(num_servers)}
    failed_requests = 0

    async def fetch(session, server_loads):
        nonlocal failed_requests
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    server_id = data.get('message').split()[-1]  # Extract server ID
                    if server_id in server_loads:
                        server_loads[server_id] += 1
                else:
                    failed_requests += 1
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}: {str(e)}")
            failed_requests += 1

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, server_loads) for _ in range(10000)]
        await asyncio.gather(*tasks)

    return server_loads, failed_requests

async def check_existing_nodes():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/rep') as response:
                if response.status == 200:
                    data = await response.json()
                    if 'message' in data and 'N' in data['message']:
                        num_replicas = data['message']['N']
                        replicas = data['message']['replicas']
                        return num_replicas, replicas
                    else:
                        print("Unexpected response format from /rep endpoint")
                else:
                    print(f"Failed to fetch existing nodes. Status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Error fetching /rep endpoint: {str(e)}")
    return 0, []

async def main():
    num_servers_range = range(2, 7)  # N from 2 to 6
    avg_loads = []
    avg_failed_requests = []

    num_replicas, existing_nodes = await check_existing_nodes()
    print(f"Existing nodes: {existing_nodes}")

    for num_servers in num_servers_range:
        if num_servers > num_replicas:
            data = {'hostnames': [f'server{num_servers}']}
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:5000/add', json=data) as response:
                    print(f"Added server{num_servers}: {await response.json()}")

        # Measure server load
        server_loads, failed_requests = await measure_server_load(num_servers)
        avg_failed_requests.append(failed_requests)

        total_requests = sum(server_loads.values())
        average_load = total_requests / num_servers
        avg_loads.append(average_load)

        print(f"Server Loads for {num_servers} Servers:")
        for server, requests_count in server_loads.items():
            print(f"{server}: {requests_count} requests")

    print(f"Average Load for {num_servers} Servers: {average_load} requests per server")
    print(f"Average Failed Requests: {avg_failed_requests}")

    # Plot average loads and average failed requests
    plt.figure(figsize=(8, 5))
    plt.plot(list(num_servers_range), avg_loads, marker='o', linestyle='-', color='b', label='Average Requests per Server')
    plt.plot(list(num_servers_range), avg_failed_requests, marker='s', linestyle='-', color='r', label='Average Failed Requests')
    plt.xlabel('Number of Servers')
    plt.ylabel('Requests')
    plt.title('Average Server Load and Average Failed Requests')
    plt.xticks(num_servers_range)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('average_server_load_and_failed_requests.png')

if __name__ == "__main__":
    asyncio.run(main())
