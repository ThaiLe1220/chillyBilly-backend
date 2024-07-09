# POSTGRESQL RUN NOTE

## Setting Up Database

### Step 1: Install PostgreSQL

sudo apt update
sudo apt install postgresql postgresql-contrib

### Step 2: Create a database

1. **Initial setup and database configuration:**

    ```bash
    sudo -u postgres psql

    CREATE DATABASE tts_app;
    CREATE USER tts_user WITH PASSWORD 'tts_eugene';
    GRANT ALL PRIVILEGES ON DATABASE tts_app TO tts_user;

    \l
    \du
    \c tts_app
    \z
    ```

2. **Clear terminal and query tables:**

    ```bash
    \! clear
    \dt

    tts_app=# \dt
                List of relations
    Schema |      Name       | Type  |  Owner   
    --------+-----------------+-------+----------
    public | api_usage       | table | tts_user
    public | error_logs      | table | tts_user
    public | generated_audio | table | tts_user
    public | sessions        | table | tts_user
    public | system_settings | table | tts_user
    public | text_entries    | table | tts_user
    public | usage_history   | table | tts_user
    public | user_feedback   | table | tts_user
    public | user_profiles   | table | tts_user
    public | users           | table | tts_user
    public | voice_clones    | table | tts_user
    (11 rows)

    \d users
    SELECT * FROM users;
    ```

### Step 3: Install Python dependencies

pip install -r requirements.txt

### Step 4: Create database schema

check ./models.py and ./main.py

Certainly! Here's an updated README with instructions to test all features in the main code:

## Testing Database Features

### User Management

**Create users:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{"username":"testuser1", "email":"testuser1@example.com", "password":"testpassword1"}'
curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{"username":"testuser2", "email":"testuser2@com.com", "password":"testpassword2"}'
curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{"username":"eugene", "email":"lehongthai2000@gmail.com", "password":"thai1220"}'
```

**Get all users:** ✅

```bash
curl "http://localhost:8000/api/v1/users/"
curl "http://localhost:8000/api/v1/users/10"
```

**Update user information:** ✅

```bash
curl -X PUT "http://localhost:8000/api/v1/users/10" -H "Content-Type: application/json" -d '{"email":"eugene2000@gmail.com", "password":"thai2000"}'
```

**Delete a user:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/11"
```

**Create a user profile:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/10/profile/" -H "Content-Type: application/json" -d '{"first_name":"Thai", "last_name":"Le", "date_of_birth":"2000-12-13T04:30:00", "preferred_language":"en"}'

curl "http://localhost:8000/api/v1/users/10/profile/"
```

**Update user profile:** ✅

```bash
curl -X PUT "http://localhost:8000/api/v1/users/10/profile/" -H "Content-Type: application/json" -d '{"first_name":"Eugene", "last_name":"LiuLiu"}'

curl "http://localhost:8000/api/v1/users/10/profile/"
```

### Text Entries

**Create a text entry:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/10/text_entries/" -H "Content-Type: application/json" -d '{"content":"Hello, world!", "language":"en"}'
```

**Get user's text entries:** ✅

```bash
curl "http://localhost:8000/api/v1/users/10/text_entries/"
```

**Delete a text entry:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1/text_entries/1"
```

### Audio Generation

**Create generated audio:**

```bash
curl -X POST "http://localhost:8000/api/v1/generated_audio/" -H "Content-Type: application/json" -d '{"text_id":1, "file_path":"/path/to/audio.mp3", "duration":3.5}'
```

**Get generated audio:**

```bash
curl "http://localhost:8000/api/v1/generated_audio/1"
```

### Voice Cloning

**Create a voice clone:**

```bash
curl -X POST "http://localhost:8000/api/v1/users/1/voice_clones/" -H "Content-Type: application/json" -d '{"original_file_path":"/path/to/original_voice.wav"}'
```

**Get user's voice clones:**

```bash
curl "http://localhost:8000/api/v1/users/1/voice_clones/"
```

**Delete a voice clone:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1/voice_clones/1"
```

### User Feedback

**Create user feedback:**

```bash
curl -X POST "http://localhost:8000/api/v1/users/1/feedback/" -H "Content-Type: application/json" -d '{"audio_id":1, "rating":5, "comment":"Great audio quality!"}'
```

**Get user feedback:**

```bash
curl "http://localhost:8000/api/v1/users/1/feedback/"
```

### System Settings

**Create a system setting:**

```bash
curl -X POST "http://localhost:8000/api/v1/system_settings/" -H "Content-Type: application/json" -d '{"key":"max_audio_length", "value":"300"}'
```

**Get a system setting:**

```bash
curl "http://localhost:8000/api/v1/system_settings/max_audio_length"
```

**Update a system setting:**

```bash
curl -X PUT "http://localhost:8000/api/v1/system_settings/max_audio_length" -H "Content-Type: application/json" -d '{"value":"600"}'
```

### API Usage Logging

**Log API usage:**

```bash
curl -X POST "http://localhost:8000/api/v1/api_usage/" -H "Content-Type: application/json" -d '{"user_id":1, "endpoint":"/users/"}'
```

**Get API usage for a user:**

```bash
curl "http://localhost:8000/api/v1/api_usage/1"
```

### Error Logging

**Log an error:**

```bash
curl -X POST "http://localhost:8000/api/v1/error_logs/" -H "Content-Type: application/json" -d '{"error_type":"ValidationError", "error_message":"Invalid input", "stack_trace":"..."}'
```

**Get all error logs:**

```bash
curl "http://localhost:8000/api/v1/error_logs/"
```

### Session Management

**Create a session:**

```bash
curl -X POST "http://localhost:8000/api/v1/sessions/" -H "Content-Type: application/json" -d '{"user_id":1}'
```

**Get a session by token (replace <token> with the actual token):**

```bash
curl "http://localhost:8000/api/v1/sessions/<token>"
```

**Delete a session:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/sessions/<token>"
```

### Usage History

**Log usage history:**

```bash
curl -X POST "http://localhost:8000/api/v1/usage_history/" -H "Content-Type: application/json" -d '{"user_id":1, "action_type":"text_entry", "related_id":1}'
```

**Get usage history for a user:**

```bash
curl "http://localhost:8000/api/v1/usage_history/1"
```

### Database Verification

To verify the database state, connect to PostgreSQL and check the tables:

**Connect to the database:****

```bash
psql -U tts_user -d tts_app
```

**List all tables:**

```sql
\dt
```

**View contents of specific tables:**

```sql
SELECT * FROM users;
SELECT * FROM user_profiles;
SELECT * FROM text_entries;
SELECT * FROM generated_audio;
SELECT * FROM voice_clones;
SELECT * FROM system_settings;
SELECT * FROM api_usage;
SELECT * FROM error_logs;
SELECT * FROM sessions;
SELECT * FROM usage_history;
SELECT * FROM user_feedback;
```
