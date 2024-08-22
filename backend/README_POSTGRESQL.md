# POSTGRESQL RUN NOTE

## Setting Up Database

### Step 1: Install PostgreSQL

sudo apt update
sudo apt install postgresql postgresql-contrib
sudo apt-get install jq
 
### Step 2: Create a database

Initial setup and database configuration:

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

### Step 3: Install Python dependencies

`pip3 install -r requirements.txt`

### Step 4: Create database

Check `models`, `schemas`, `routers` directories and `database.py`

## Testing Database Features

Run the app `python3 app.py`

### User Management

**Create users:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"username":"eugene", "email":"lehongthai2000@gmail.com", "password":"thai1220", "role":"REGULAR"}'

curl -X POST "https://face-swap.12pmtech.link/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"username":"mrdnlove", "email":"thailehong1220@yahoo.com", "password":"mrdnlove", "role":"ADMIN"}'
```

**Get all users:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/users/"
curl "https://face-swap.12pmtech.link/api/v1/users/1"
```

**Update user information:** ✅

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/users/1" \
     -H "Content-Type: application/json" \
     -d '{"username":"eu", "email":"eu@ex.com", "password":"eu123", "is_active": true, "role":"ADMIN"}'
```

**Verify user password:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/users/1/verify_password" \
     -H "Content-Type: application/json" \
     -d '{"password":"eu123"}'
```

**Delete a user:** ✅

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/users/2"
```

**Create a user profile:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/users/1/profile/" \
     -H "Content-Type: application/json" \
     -d '{"first_name":"Thai", "last_name":"Le", "date_of_birth":"2000-12-13T04:30:00", "preferred_language":"en"}'
```

**Get user profile:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/users/1/profile/"
```

**Update user profile:** ✅

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/users/1/profile/" \
     -H "Content-Type: application/json" \
     -d '{"first_name":"Eugene", "last_name":"LiuLiu"}'
```

### Guest Management

**Create guest session:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/guests"
```

**Get all guests:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/guests"
```

**Get specific guest information:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/guests/1"
```

**Update guest activity:**

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/guests/1"
```

**Delete a guest:**

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/guests/1"
```

**Cleanup inactive guests:**

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/guests/cleanup/"
```

### Text Entries

**Create a text entry (user):** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/text_entries/" \
     -H "Content-Type: application/json" \
     -d '{"content":"Hello, world!", "language":"en", "user_id":1}'
```

**Create a text entry (guest):** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/text_entries/" \
     -H "Content-Type: application/json" \
     -d '{"content":"Hello from guest!", "language":"en", "guest_id":1}'
```

**Get text entries for a specific user:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/users/1/text_entries/"
curl "https://face-swap.12pmtech.link/api/v1/text_entries/?user_id=1"

```

**Get text entries for a specific guest:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/guests/1/text_entries/"
curl "https://face-swap.12pmtech.link/api/v1/text_entries/?guest_id=1"

```

**Get all text entries:** ✅

```bash
# Get the first 10 text entries
curl "https://face-swap.12pmtech.link/api/v1/all_text_entries/"

# Get the next 10 text entries
curl "https://face-swap.12pmtech.link/api/v1/all_text_entries/?skip=10"

# Get 20 text entries at once
curl "https://face-swap.12pmtech.link/api/v1/all_text_entries/?limit=20"
```

**Get a specific text entry:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/text_entries/1"
```

**Delete a text entry:** ✅

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/text_entries/2"
```

### Voice Management

**Create default voices:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/voices/create_defaults/"
```

**Create a voice:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/users/1/voices/" \
  -H "Content-Type: application/json" \
  -d '{
    "voice_name": "MyVoice",
    "original_file_path": "/path/to/original_voice.wav",
    "language": "en",
    "description": "My custom voice"
  }'
```

**Get all voices:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/voices/?skip=0&limit=10"
```

**Get user's voices (including default voices):** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/users/10/voices/?skip=0&limit=10"
```

**Get a specific voice:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/voices/1"
```

**Update a voice:** ✅

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/users/1/voices/2" \
     -H "Content-Type: application/json" \
     -d '{
         "voice_name": "Updated Voice Name",
         "language": "en",
         "description": "This is an updated description",
         "original_file_path": "/updated/path/to/audio/file.mp3"
     }'
```

**Delete a voice:** ✅

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/users/1/voices/5"
```

### Audio Management

**Create audio:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/audios/" \
     -H "Content-Type: application/json" \
     -d '{"text_entry_id":1, "voice_id":1}'
```

**Get specific audio:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/audios/1"
```

**Get audios for a specific user or guest:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/audios/?user_id=1"
curl "https://face-swap.12pmtech.link/api/v1/audios/?guest_id=1"
```

**Get all audios:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/all-audios/"
```

**Delete audio:** ✅

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/audios/1"
```

### User Feedback Management

**Create user feedback:** ✅

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/users/1/feedback" \
     -H "Content-Type: application/json" \
     -d '{"audio_id": 1, "rating": 5, "comment": "Great audio quality!"}'
```

**Get specific feedback:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/feedback/1"
```

**Get all feedback for a specific user:** ✅

```bash
curl "https://face-swap.12pmtech.link/api/v1/users/1/feedback"
```

**Update existing feedback:** ✅

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/feedback/1" \
     -H "Content-Type: application/json" \
     -d '{"rating": 4, "comment": "Good audio, but could be better."}'
```

**Delete feedback:** ✅

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/feedback/1"
```

### System Settings

**Create a system setting:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/system_settings/" -H "Content-Type: application/json" -d '{"key":"max_audio_length", "value":"300"}'
```

**Get a system setting:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/system_settings/max_audio_length"
```

**Update a system setting:**

```bash
curl -X PUT "https://face-swap.12pmtech.link/api/v1/system_settings/max_audio_length" -H "Content-Type: application/json" -d '{"value":"600"}'
```

### API Usage Logging

**Log API usage:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/api_usage/" -H "Content-Type: application/json" -d '{"user_id":1, "endpoint":"/users/"}'
```

**Get API usage for a user:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/api_usage/1"
```

### Error Logging

**Log an error:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/error_logs/" -H "Content-Type: application/json" -d '{"error_type":"ValidationError", "error_message":"Invalid input", "stack_trace":"..."}'
```

**Get all error logs:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/error_logs/"
```

### Session Management

**Create a session:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/sessions/" -H "Content-Type: application/json" -d '{"user_id":1}'
```

**Get a session by token (replace <token> with the actual token):**

```bash
curl "https://face-swap.12pmtech.link/api/v1/sessions/<token>"
```

**Delete a session:**

```bash
curl -X DELETE "https://face-swap.12pmtech.link/api/v1/sessions/<token>"
```

### Usage History

**Log usage history:**

```bash
curl -X POST "https://face-swap.12pmtech.link/api/v1/usage_history/" -H "Content-Type: application/json" -d '{"user_id":1, "action_type":"text_entry", "related_id":1}'
```

**Get usage history for a user:**

```bash
curl "https://face-swap.12pmtech.link/api/v1/usage_history/1"
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
SELECT * FROM guests;
SELECT * FROM user_profiles;
SELECT * FROM generated_audio;
SELECT * FROM text_entries;
SELECT * FROM voice_clones;
SELECT * FROM user_feedback;

SELECT * FROM system_settings;
SELECT * FROM api_usage;
SELECT * FROM error_logs;
SELECT * FROM sessions;
SELECT * FROM usage_history;
```

**Other SQL query to interact with the tables:**

```sql
DELETE FROM users WHERE id = 1;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS guests;
DROP TABLE IF EXISTS user_profiles;
DROP TABLE IF EXISTS generated_audio;
DROP TABLE IF EXISTS text_entries;
DROP TABLE IF EXISTS voice_clones;
DROP TABLE IF EXISTS user_feedback;
DROP TABLE IF EXISTS system_settings;
DROP TABLE IF EXISTS api_usage;
DROP TABLE IF EXISTS error_logs;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS usage_history;
```
