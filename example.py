import asyncio
import os
import getpass
from boostcampapi import BoostcampAPI, BoostcampAuthException, LoginFailedException

async def main():
    api = BoostcampAPI()
    
    # 1. Try to load an existing session
    if api.load_session():
        print("Loaded existing session from .boostcamp/session.pickle")
    else:
        # 2. If no session, try to login with credentials
        email = os.environ.get("BOOSTCAMP_EMAIL")
        password = os.environ.get("BOOSTCAMP_PASSWORD")
        
        if not email or not password:
            print("No saved session found and BOOSTCAMP_EMAIL/PASSWORD not set.")
            email = input("Enter Boostcamp Email: ")
            password = getpass.getpass("Enter Boostcamp Password: ")
            
        try:
            print(f"Logging in as {email}...")
            await api.login(email, password)
            print("Login successful! Session saved.")
        except LoginFailedException as e:
            print(f"Login failed: {e}")
            return

    # 3. Use the API
    try:
        print("\nFetching user profile...")
        profile = await api.get_user_profile()
        print(f"Successfully connected as: {profile['data']['name']}")
        
        print("\nFetching user programs...")
        programs = await api.list_user_programs()
        rows = programs.get('data', {}).get('rows', [])
        print(f"Number of user programs: {len(rows)}")
        for program in rows:
            print(f"- {program.get('title', 'Untitled')}")
            
    except BoostcampAuthException as e:
        print(f"Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
