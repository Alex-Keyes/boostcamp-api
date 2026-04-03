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

        print("\nFetching training history...")
        history = await api.get_training_history()
        dates = sorted(history.get('data', {}).keys(), reverse=True)
        print(f"Number of days with workouts: {len(dates)}")
        for date in dates[:3]:  # Show last 3 days with workouts
            workouts = history['data'][date]
            print(f"\nDate: {date}")
            for workout in workouts:
                print(f"  Workout: {workout.get('name')} ({workout.get('title')})")
                for record in workout.get('records', []):
                    print(f"    - {record.get('name')}: {len(record.get('sets', []))} sets")

        print("\nFetching custom exercises...")
        custom_exercises = await api.list_custom_exercises()
        exercises = custom_exercises.get('data', [])
        print(f"Number of custom exercises: {len(exercises)}")
        for exercise in exercises[:5]:
            print(f"- {exercise.get('name')}")
            
    except BoostcampAuthException as e:
        print(f"Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
