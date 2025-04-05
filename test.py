import httpx
import asyncio
import json

async def main():
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': 'fdfe4dddda24b09791246b8fc8aa268bc8d7903e',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "q": "apple inc",
        "num": 2,
    })

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        print(response.text)

# Run the async main
asyncio.run(main())

