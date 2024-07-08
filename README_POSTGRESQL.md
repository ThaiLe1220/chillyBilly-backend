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

pip install fastapi uvicorn sqlalchemy psycopg2-binary

### Step 4: Create database schema

check ./models.py and ./main.py

Certainly! Here's an updated README with instructions to test all features in the main code:

## Testing Database Features

### User Management

1. Create users:

   ```bash
   curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username":"testuser1", "email":"test1@example.com", "password":"password123"}'
   curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username":"testuser2", "email":"testuser2@com.com", "password":"testpassword2"}'
   ```

2. Get all users:

   ```bash
   curl "http://localhost:8000/users/"
   ```

3. Update user information:

   ```bash
   curl -X PUT "http://localhost:8000/users/1" -H "Content-Type: application/json" -d '{"email":"newemail@example.com"}'
   ```

4. Delete a user:

   ```bash
   curl -X DELETE "http://localhost:8000/users/2"
   ```

5. Create a user profile:

   ```bash
   curl -X POST "http://localhost:8000/users/1/profile/" -H "Content-Type: application/json" -d '{"first_name":"John", "last_name":"Doe", "date_of_birth":"1990-01-01T00:00:00", "preferred_language":"en"}'
   ```

6. Update user profile:

   ```bash
   curl -X PUT "http://localhost:8000/users/1/profile/" -H "Content-Type: application/json" -d '{"first_name":"Jane", "last_name":"Doe"}'
   ```

### Text Entries

7. Create a text entry:

   ```bash
   curl -X POST "http://localhost:8000/users/1/text_entries/" -H "Content-Type: application/json" -d '{"content":"Hello, world!", "language":"en"}'
   ```

8. Get user's text entries:

   ```bash
   curl "http://localhost:8000/users/1/text_entries/"
   ```

9. Delete a text entry:

   ```bash
   curl -X DELETE "http://localhost:8000/users/1/text_entries/1"
   ```

### Audio Generation

10. Create generated audio:

    ```bash
    curl -X POST "http://localhost:8000/generated_audio/" -H "Content-Type: application/json" -d '{"text_id":1, "file_path":"/path/to/audio.mp3", "duration":3.5}'
    ```

11. Get generated audio:

    ```bash
    curl "http://localhost:8000/generated_audio/1"
    ```

### Voice Cloning

12. Create a voice clone:

    ```bash
    curl -X POST "http://localhost:8000/users/1/voice_clones/" -H "Content-Type: application/json" -d '{"original_file_path":"/path/to/original_voice.wav"}'
    ```

13. Get user's voice clones:

    ```bash
    curl "http://localhost:8000/users/1/voice_clones/"
    ```

14. Delete a voice clone:

    ```bash
    curl -X DELETE "http://localhost:8000/users/1/voice_clones/1"
    ```

### User Feedback

15. Create user feedback:

    ```bash
    curl -X POST "http://localhost:8000/users/1/feedback/" -H "Content-Type: application/json" -d '{"audio_id":1, "rating":5, "comment":"Great audio quality!"}'
    ```

16. Get user feedback:

    ```bash
    curl "http://localhost:8000/users/1/feedback/"
    ```

### System Settings

17. Create a system setting:

    ```bash
    curl -X POST "http://localhost:8000/system_settings/" -H "Content-Type: application/json" -d '{"key":"max_audio_length", "value":"300"}'
    ```

18. Get a system setting:

    ```bash
    curl "http://localhost:8000/system_settings/max_audio_length"
    ```

19. Update a system setting:

    ```bash
    curl -X PUT "http://localhost:8000/system_settings/max_audio_length" -H "Content-Type: application/json" -d '{"value":"600"}'
    ```

### API Usage Logging

20. Log API usage:

    ```bash
    curl -X POST "http://localhost:8000/api_usage/" -H "Content-Type: application/json" -d '{"user_id":1, "endpoint":"/users/"}'
    ```

21. Get API usage for a user:

    ```bash
    curl "http://localhost:8000/api_usage/1"
    ```

### Error Logging

22. Log an error:

    ```bash
    curl -X POST "http://localhost:8000/error_logs/" -H "Content-Type: application/json" -d '{"error_type":"ValidationError", "error_message":"Invalid input", "stack_trace":"..."}'
    ```

23. Get all error logs:

    ```bash
    curl "http://localhost:8000/error_logs/"
    ```

### Session Management

24. Create a session:

    ```bash
    curl -X POST "http://localhost:8000/sessions/" -H "Content-Type: application/json" -d '{"user_id":1}'
    ```

25. Get a session by token (replace <token> with the actual token):

    ```bash
    curl "http://localhost:8000/sessions/<token>"
    ```

26. Delete a session:

    ```bash
    curl -X DELETE "http://localhost:8000/sessions/<token>"
    ```

### Usage History

27. Log usage history:

    ```bash
    curl -X POST "http://localhost:8000/usage_history/" -H "Content-Type: application/json" -d '{"user_id":1, "action_type":"text_entry", "related_id":1}'
    ```

28. Get usage history for a user:

    ```bash
    curl "http://localhost:8000/usage_history/1"
    ```

### Database Verification

To verify the database state, connect to PostgreSQL and check the tables:

1. Connect to the database:

   ```bash
   psql -U tts_user -d tts_app
   ```

2. List all tables:

   ```sql
   \dt
   ```

3. View contents of specific tables:

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
