import httpx, json, random
import asyncio
from datetime import datetime

async def get_url(client, url, headers):
    resp = await client.get(url, headers=headers)
    print(resp.http_version)
    return resp.text

async def main():
    limits = httpx.Limits(max_keepalive_connections=1, max_connections=1)
    client = httpx.AsyncClient(http2=True, verify=False, timeout=3.0, limits=limits)
    headers = {"x-foo": "bar"}
    workers = []
    # host = "https://httpbin.org"
    # host = "http://localhost:8080"
    host = "https://localhost:8443"
    delay_url = f"{host}/delay"
    bytes_url = f"{host}/bytes"
    start = datetime.now()
    for i in range(10):
        url = f"{bytes_url}/{random.randint(1000,99999)}"
        workers.append(get_url(client, url=url, headers=headers))
    resps = await asyncio.gather(*workers)
    for i in range(len(resps)):
        print(f"{i}: {len(resps[i])}")
    end = datetime.now()
    print(f"duration: {end - start}")
    await client.aclose()    

asyncio.run(main())