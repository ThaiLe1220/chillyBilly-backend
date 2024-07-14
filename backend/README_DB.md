# Summary of database architecture

tts_app/
├── backend/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── guest.py
│   │   ├── user_profile.py
│   │   ├── text_entry.py
│   │   ├── voice.py
│   │   ├── audio.py
│   │   └── user_feedback.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── guest.py
│   │   ├── user_profile.py
│   │   ├── text_entry.py
│   │   ├── voice.py
│   │   ├── audio.py
│   │   └── user_feedback.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── guests.py
│   │   ├── user_profiles.py
│   │   ├── text_entries.py
│   │   ├── voices.py
│   │   ├── audios.py
│   │   └── user_feedback.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── guest_service.py
│   │   ├── user_profile_service.py
│   │   ├── text_entry_service.py
│   │   ├── voice_service.py
│   │   ├── audio_service.py
│   │   ├── user_feedback_service.py
│   ├── app.py
│   ├── database.py
│   ├── Dockerfile.yml
│   └── requirements.txt
├── .env
├── .gitignore
├── docker-compose.yml

## Database Tables

1. User
2. UserProfile
3. Session
4. TextEntry
5. Audio
6. Voice
7. UsageHistory
8. ErrorLog
9. APIUsage
10. UserFeedback
11. SystemSetting

## Additional Aspects

1. **Authentication:**
   - TwoFactorEnabled field in the Users table.

2. **Error Logging:**
   - ErrorLogs table for system monitoring.

3. **API Limits:**
   - APIUsage table to track rate limits.

4. **User Feedback:**
   - UserFeedback table for audio quality ratings.

5. **System Settings:**
   - SystemSettings table for global configurations.

6. **Backups:**
   - Implement regular database backups.

7. **Data Retention:**
   - LastActiveDate field in the Users table for archiving/deletion.

8. **Performance:**
   - Index key fields (e.g., UserID, CreatedAt).

9. **Localization:**
   - Ensure Language fields can accommodate future expansion.

### Full Architecture

## User Table

- **Description**: Stores basic user information and handles authentication details.
- **Columns**:
  - **UserID (PK)**: Unique identifier for the user.
  - **Username**: The user's chosen username.
  - **Email**: The user's email address.
  - **PasswordHash**: The hashed password for security.
  - **TwoFactorEnabled**: Indicates if two-factor authentication is enabled.
  - **CreatedAt**: Timestamp of user creation.
  - **LastLogin**: Timestamp of the last login.
  - **LastActiveDate**: Timestamp of the last activity for data retention purposes.

## UserProfile Table

- **Description**: Stores additional profile information for users.
- **Columns**:
  - **ProfileID (PK)**: Unique identifier for the profile.
  - **UserID (FK)**: References the user.
  - **FirstName**: The user's first name.
  - **LastName**: The user's last name.
  - **DateOfBirth**: The user's date of birth.
  - **PreferredLanguage**: The user's preferred language.

## Session Table

- **Description**: Tracks active user sessions and session details.
- **Columns**:
  - **SessionID (PK)**: Unique identifier for the session.
  - **UserID (FK)**: References the user.
  - **Token**: Session token.
  - **StartTime**: Session start time.
  - **ExpiryTime**: Session expiry time.
  - **LastActivity**: Timestamp of the last activity in the session.

## TextEntry Table

- **Description**: Stores text entries input by users for conversion to audio.
- **Columns**:
  - **TextID (PK)**: Unique identifier for the text entry.
  - **UserID (FK)**: References the user.
  - **Content**: The text content.
  - **Language**: Language of the text content.
  - **CreatedAt**: Timestamp of text entry creation.

## Audio Table

- **Description**: Stores information about the audio files generated from text entries.
- **Columns**:
  - **AudioID (PK)**: Unique identifier for the generated audio.
  - **TextID (FK)**: References the text entry.
  - **UserID (FK)**: References the user.
  - **FilePath**: Path to the audio file.
  - **Duration**: Duration of the audio.
  - **CreatedAt**: Timestamp of audio generation.

## Voice Table

- **Description**: Stores information about voice clones created by users.
- **Columns**:
  - **CloneID (PK)**: Unique identifier for the voice clone.
  - **UserID (FK)**: References the user.
  - **OriginalFilePath**: Path to the original audio file.
  - **ProcessedFilePath**: Path to the processed audio file.
  - **Status**: Status of the voice clone process.
  - **CreatedAt**: Timestamp of voice clone creation.

## UsageHistory Table

- **Description**: Records the history of user actions and usage within the application.
- **Columns**:
  - **HistoryID (PK)**: Unique identifier for the usage history.
  - **UserID (FK)**: References the user.
  - **ActionType**: Type of action performed.
  - **RelatedID**: Identifier related to the action.
  - **Timestamp**: Timestamp of the action.

## ErrorLog Table

- **Description**: Logs errors for system monitoring and troubleshooting.
- **Columns**:
  - **LogID (PK)**: Unique identifier for the error log.
  - **Timestamp**: Timestamp of the error.
  - **ErrorType**: Type of error.
  - **ErrorMessage**: Error message.
  - **StackTrace**: Stack trace of the error.

## APIUsage Table

- **Description**: Tracks API usage and enforces rate limits.
- **Columns**:
  - **UsageID (PK)**: Unique identifier for the API usage.
  - **UserID (FK)**: References the user.
  - **Endpoint**: API endpoint accessed.
  - **RequestCount**: Number of requests made.
  - **LastRequest**: Timestamp of the last request.
  - **DailyLimit**: Daily request limit.

## UserFeedback Table

- **Description**: Stores feedback from users about the generated audio quality.
- **Columns**:
  - **FeedbackID (PK)**: Unique identifier for the feedback.
  - **UserID (FK)**: References the user.
  - **AudioID (FK)**: References the audio.
  - **Rating**: Rating given by the user.
  - **Comment**: Feedback comment.
  - **CreatedAt**: Timestamp of feedback submission.

## SystemSetting Table

- **Description**: Stores global configuration settings for the application.
- **Columns**:
  - **SettingID (PK)**: Unique identifier for the setting.
  - **SettingKey**: Key for the setting.
  - **SettingValue**: Value for the setting.
  - **LastUpdated**: Timestamp of the last update.
