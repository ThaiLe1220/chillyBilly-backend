# POSTGRESQL RUN NOTE

## Setting Up Database

### Step 1: Install PostgreSQL

sudo apt update
sudo apt install postgresql postgresql-contrib

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

Certainly! I'll update the README section to test all the implemented routes, including the new guest functionality and the updated audio generation process. Here's the revised version:

### User Management

**Create users:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{"username":"eugene", "email":"lehongthai2000@gmail.com", "password":"thai1220"}'
curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{"username":"mrdnlove", "email":"thailehong1220@yahoo.com", "password":"mrdnlove"}'
```

**Get all users:** ✅

```bash
curl "http://localhost:8000/api/v1/users/"
curl "http://localhost:8000/api/v1/users/1"
```

**Update user information:** ✅

```bash
curl -X PUT "http://localhost:8000/api/v1/users/3" \
     -H "Content-Type: application/json" \
     -d '{"username":"eu", "email":"eu@ex.com", "password":"eu123"}'
```

**Verify user password:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/3/verify_password" \
     -H "Content-Type: application/json" \
     -d '{"password":"eu123"}'
```

**Delete a user:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/2"
```

**Create a user profile:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/5/profile/" -H "Content-Type: application/json" -d '{"first_name":"Thai", "last_name":"Le", "date_of_birth":"2000-12-13T04:30:00", "preferred_language":"en"}'
```

**Get user profile:** ✅

```bash
curl "http://localhost:8000/api/v1/users/5/profile/"
```

**Update user profile:** ✅

```bash
curl -X PUT "http://localhost:8000/api/v1/users/5/profile/" -H "Content-Type: application/json" -d '{"first_name":"Eugene", "last_name":"LiuLiu"}'
```

### Guest Management

**Create or get guest session:** ✅

```bash
curl "http://localhost:8000/api/v1/guests/session"
```

**Get guest information:** ✅

```bash
curl "http://localhost:8000/api/v1/guests"

curl "http://localhost:8000/api/v1/guests/1"

```

**Update guest activity:** ✅

```bash
curl -X PUT "http://localhost:8000/api/v1/guests/1/active"
```

### Text Entries

Here's the updated README markdown for text entries based on the changes we discussed:

### Text Entries

**Create a text entry (user):** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/text_entries/" \
     -H "Content-Type: application/json" \
     -d '{"content":"Hello, world!", "language":"en", "user_id":5}'
```

**Create a text entry (guest):** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/text_entries/" \
     -H "Content-Type: application/json" \
     -d '{"content":"Hello from guest!", "language":"en", "guest_id":2}'
```

**Get text entries for a specific user:** ✅

```bash
curl "http://localhost:8000/api/v1/users/5/text_entries/"
curl "http://localhost:8000/api/v1/text_entries/?user_id=5"

```

**Get text entries for a specific guest:** ✅

```bash
curl "http://localhost:8000/api/v1/guests/1/text_entries/"
curl "http://localhost:8000/api/v1/text_entries/?guest_id=1"

```

**Get all text entries:** ✅

```bash
# Get the first 10 text entries
curl "http://localhost:8000/api/v1/all_text_entries/"

# Get the next 10 text entries
curl "http://localhost:8000/api/v1/all_text_entries/?skip=10"

# Get 20 text entries at once
curl "http://localhost:8000/api/v1/all_text_entries/?limit=20"
```

**Get a specific text entry:** ✅

```bash
curl "http://localhost:8000/api/v1/text_entries/1"
```

**Delete a text entry:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/text_entries/7"
```

### Audio Generation

**Create generated audio (user):** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/audios/" -H "Content-Type: application/json" -d '{"text_entry_id":1, "file_path":"/path/to/audio.mp3", "duration":3.5}'
```

**Create generated audio (user with voice clone):** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/audios/" -H "Content-Type: application/json" -d '{"text_entry_id":1, "voice_clone_id":1, "file_path":"/path/to/audio.mp3", "duration":3.5}'
```

**Create generated audio (guest):** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/audios/" -H "Content-Type: application/json" -d '{"text_entry_id":2, "file_path":"/path/to/audio.mp3", "duration":3.5}'
```

**Get generated audio:** ✅

```bash
curl "http://localhost:8000/api/v1/audios/1"
```

**Get user's generated audios:** ✅

```bash
curl "http://localhost:8000/api/v1/audios/?user_id=10"
```

**Get guest's generated audios:** ✅

```bash
curl "http://localhost:8000/api/v1/audios/?guest_id={guest_id}"
```

**Delete generated audio:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/audios/1"
```

### Voice Cloning

**Create a voice clone:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/10/voice_clones/" -H "Content-Type: application/json" -d '{"voice_name":"MyVoice", "original_file_path":"/path/to/original_voice.wav"}'
```

**Get a specific voice clone:** ✅

```bash
curl "http://localhost:8000/api/v1/voice_clones/1"
```

**Get user's voice clones:** ✅

```bash
curl "http://localhost:8000/api/v1/users/10/voice_clones/"
```

**Delete a voice clone:** ✅

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/10/voice_clones/1"
```

### User Feedback

**Create user feedback:** ✅

```bash
curl -X POST "http://localhost:8000/api/v1/users/10/feedback/" -H "Content-Type: application/json" -d '{"audio_id":1, "rating":5, "comment":"Great audio quality!"}'
```

**Get user feedback:** ✅

```bash
curl "http://localhost:8000/api/v1/users/10/feedback/"
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
```
