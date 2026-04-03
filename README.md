# Boostcamp API

An unofficial, asynchronous Python client for the Boostcamp fitness app API. Modeled after the popular `monarchmoney` Python client.

## Requirements
- Python 3.8+
- `aiohttp`

## Installation
Currently in development. You can install it locally:
```bash
pip install -e .
```

## Usage
The API uses your Boostcamp FirebaseIdToken for authentication.

```python
import asyncio
import os
from boostcampapi import BoostcampAPI

async def main():
    token = os.environ.get("BOOSTCAMP_TOKEN")
    api = BoostcampAPI(token)
    
    # Get user profile
    profile = await api.get_user_profile()
    print(profile)

    # Get user programs
    programs = await api.list_user_programs()
    print(programs)

if __name__ == "__main__":
    asyncio.run(main())
```

## Obtaining a Token
You can extract your `FirebaseIdToken` by logging into the Boostcamp web app (https://www.boostcamp.app) and inspecting the network tab in your browser's developer tools for any API requests sent to `newapi.boostcamp.app`. The token is sent in the `Authorization` header.
