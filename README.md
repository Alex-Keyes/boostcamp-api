# 🏋️‍♂️ Boostcamp API: Gainz for your Python Scripts

An unofficial, asynchronous Python client for the [Boostcamp](https://www.boostcamp.app/) fitness app API. Because your data deserves a heavy lifting session too! 🚀

Modeled after the sleek `monarchmoney` client, this library lets you pull your workout data, training history, and program details without breaking a sweat.

## ✨ Features

- **Asynchronous & Fast:** Built on `aiohttp` for maximum performance.
- **Full History:** Get every rep and set you've ever logged. 📈
- **Program Discovery:** Search the entire Boostcamp library for your next challenge.
- **Dashboard Stats:** Track your streaks, total volume, and muscle distribution. 🦾
- **Session Persistence:** Login once, save your session, and stay authenticated.

## 🛠 Requirements

- Python 3.8+
- `aiohttp` (The heavy lifter)

## 🚀 Quick Start

### Installation

```bash
# Clone and install in editable mode
pip install -e .
```

### Basic Usage

```python
import asyncio
from boostcampapi import BoostcampAPI

async def main():
    api = BoostcampAPI()
    
    # Login (or load a saved session)
    if not api.load_session():
        await api.login("beast@mode.com", "lightweight_baby")
    
    # Get your dashboard summary
    summary = await api.get_home_summary()
    print(f"🔥 Current Streak: {summary['data']['week_streak']} weeks")
    
    # Fetch your lifting history
    history = await api.get_training_history()
    print(f"📚 You've logged {len(history['data'])} days of workouts!")

asyncio.run(main())
```

## 🔐 Authentication Note (Google/Apple Users)

If you usually tap the Google or Apple button to log in, you'll need to set a "traditional" password to use this API:

1. Head to the [Boostcamp Login Page](https://www.boostcamp.app/login).
2. Enter your email and click **"Forgot Password?"**.
3. Set your new password via the email link.
4. Use those credentials to start scripting! 🔓

## 📊 Discovered Endpoints

Check out [BOOSTCAMP_API.md](./BOOSTCAMP_API.md) for the full breakdown of everything we've reverse-engineered so far.

## 🤝 Contributing

Found a new endpoint? Want to add a feature? Open a PR! Let's build the ultimate tool for data-driven athletes. 🤝

---
*Disclaimer: This is an unofficial project and is not affiliated with Boostcamp. Use responsibly and don't be a jerk to their servers.*
