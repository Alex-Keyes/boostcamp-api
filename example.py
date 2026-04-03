import asyncio
import os
from boostcampapi import BoostcampAPI, BoostcampAuthException

async def main():
    # Token from environment variable
    token = os.environ.get("BOOSTCAMP_TOKEN")
    
    if not token:
        print("Error: BOOSTCAMP_TOKEN environment variable not set.")
        print("Please provide a fresh FirebaseIdToken.")
        return

    api = BoostcampAPI(token)
    
    try:
        print("Fetching user profile...")
        profile = await api.get_user_profile()
        print(f"Successfully connected as: {profile['data']['name']}")
        
        print("\nFetching user programs...")
        programs = await api.list_user_programs()
        rows = programs.get('data', {}).get('rows', [])
        print(f"Number of user programs: {len(rows)}")
        for program in rows:
            print(f"- {program.get('title', 'Untitled')}")
            
    except BoostcampAuthException as e:
        print(e)
        print("Please log in to the Boostcamp web app and extract a fresh 'authorization' header.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
