# Boostcamp API Documentation (Reverse Engineered)

## Base URL
`https://newapi.boostcamp.app/api/www/`

## Authentication
Authentication is handled via a Firebase ID Token passed in the `authorization` header.

**Header Format:**
`authorization: FirebaseIdToken:<YOUR_TOKEN>`

## Endpoints

### 1. Get User Profile
- **URL:** `/users/get`
- **Method:** `POST` (surprisingly, uses POST with empty body or metadata)
- **Description:** Returns detailed information about the logged-in user, including preferences, recent exercises, and exercise history.

### 2. List User Programs
- **URL:** `/user_programs/list`
- **Method:** `POST`
- **Body:** `{}`
- **Description:** Returns a list of programs the user is currently enrolled in or has completed.

### 3. Create/Log User Exercise
- **URL:** `/user_exercise/create`
- **Method:** `POST`
- **Description:** Likely used to log a completed exercise or set.

### 4. Create Program (User)
- **URL:** `/programs/my-programs/create-program`
- **Method:** `POST`

### 5. Other Potential Endpoints
Found in source code:
- `user/updateCode`
- `user/config/create`
- `user/create_firebase_custom_token`
- `stripe/payment_intent/create-checkout-session`

## Data Models (Observed)

### User Profile (`/users/get`)
- `id`: User UUID
- `name`: Full name
- `email`: Email address
- `recent_exercises`: List of recent exercise objects
- `preference`: Dictionary of user settings (weightUnit, trainingGoal, etc.)
- `user_config_list`: List of configuration objects
