# Boostcamp API Documentation (Reverse Engineered)

## Base URL
`https://newapi.boostcamp.app/api/www/`

## Authentication
Authentication is handled via a Firebase ID Token passed in the `authorization` header.

### Manual Token Retrieval
1. Log in to the Boostcamp web app.
2. Inspect the network tab for requests to `newapi.boostcamp.app`.
3. Extract the `Authorization` header value: `FirebaseIdToken:<YOUR_TOKEN>`.

### Automated Login (Re-engineered)
The app uses the Firebase Identity Toolkit to exchange credentials for a token.

#### 1. Login
- **Endpoint:** `https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=<API_KEY>`
- **API Key:** `AIzaSyAEJcoGF-5ueF3bvaujcJm2PUV7RHKQwTw`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "email": "USER_EMAIL",
    "password": "USER_PASSWORD",
    "returnSecureToken": true
  }
  ```
- **Response:** Returns `idToken`, which is used in the `Authorization` header.

#### 2. Request Password Reset (For OAuth Users)
- **Endpoint:** `https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=<API_KEY>`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "requestType": "PASSWORD_RESET",
    "email": "USER_EMAIL"
  }
  ```

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

### 4. List Custom Exercises
- **URL:** `/user_exercise/list`
- **Method:** `POST`
- **Description:** Returns a list of custom exercises created by the user.

### 5. Get Training History
- **URL:** `/programs/history`
- **Method:** `POST`
- **Payload:** `{"timezone_offset": -300}`
- **Description:** Returns the user's training history, grouped by date.

### 6. Get Payment History
- **URL:** `/users/payment_history_get`
- **Method:** `POST`
- **Description:** Returns the user's subscription and order history.

### 7. List All Programs
- **URL:** `/programs/list`
- **Method:** `POST`
- **Payload:** `{"page": 1, "pageSize": 10, "keyword": "strength"}`
- **Description:** Returns a paginated list of all available programs on Boostcamp.

### 8. Get Program Details
- **URL:** `/programs/get`
- **Method:** `POST`
- **Payload:** `{"id": "PROGRAM_UUID"}`
- **Description:** Returns detailed information about a specific program.

### 9. List Blog Posts
- **URL:** `/blogs/list`
- **Method:** `POST`
- **Payload:** `{"page": 1, "pageSize": 10}`
- **Description:** Returns a paginated list of blog posts.

### 10. Get Home Summary
- **URL:** `/home/topSection`
- **Method:** `POST`
- **Payload:** `{"timezone_offset": -300}`
- **Description:** Returns dashboard summary statistics like total workouts, total hours, and week streak.

### 11. Get Home Programs
- **URL:** `/home/programs`
- **Method:** `POST`
- **Payload:** `{"timezone_offset": -300}`
- **Description:** Returns a summary of active or recently used programs.

### 12. Get Home Volume Chart
- **URL:** `/home/chart`
- **Method:** `POST`
- **Payload:** `{"timezone_offset": -300}`
- **Description:** Returns total training volume data points for charting.

### 13. Get Home Muscle Distribution
- **URL:** `/home/muscle`
- **Method:** `POST`
- **Payload:** `{"timezone_offset": -300}`
- **Description:** Returns data on the distribution of work across different muscle groups.

### 14. Create Program (User)
- **URL:** `/programs/my-programs/create-program`
- **Method:** `POST`

### 15. Other Potential Endpoints
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
