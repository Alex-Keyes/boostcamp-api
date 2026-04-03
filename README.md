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
**Note:** This library requires a standard Boostcamp **email and password**. It does not support direct OAuth (Google/Apple) login.

### Note for OAuth Users (Google/Apple Login)
If you normally log in via Google or Apple, you **must** set a password for your account to use this API:
1. Go to the [Boostcamp Login Page](https://www.boostcamp.app/login).
2. Enter your email and click **"Forgot Password?"**.
3. Follow the link in your email to set a password.
4. Use that email and new password with this library.

Alternatively, you can trigger the reset email via this library:
```python
from boostcampapi import BoostcampAPI
import asyncio

async def reset():
    api = BoostcampAPI()
    await api.request_password_reset("your-email@example.com")

asyncio.run(reset())
```

### Basic Example
```python
import asyncio
import os
from boostcampapi import BoostcampAPI
...
## Obtaining a Token
You can extract your `FirebaseIdToken` by logging into the Boostcamp web app (https://www.boostcamp.app) and inspecting the network tab in your browser's developer tools for any API requests sent to `newapi.boostcamp.app`. The token is sent in the `Authorization` header.
