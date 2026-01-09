from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle

def upload_to_youtube(video_path, title, description, tags):
    """Upload video to YouTube using OAuth2"""
    
    # YouTube API setup
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    # Get credentials
    creds = None
    
    # Try to load existing credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, use environment variables (for GitHub Actions)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For GitHub Actions, use service account or stored token
            creds = get_credentials_from_env()
    
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    
    # Upload video
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description + "\n\n#shorts #facts #psychology #space #history",
                "tags": tags,
                "categoryId": "27"  # Education category
            },
            "status": {
                "privacyStatus": "private",  # Can change to "public" or "unlisted"
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    
    response = request.execute()
    video_id = response['id']
    video_url = f"https://youtube.com/shorts/{video_id}"
    
    return video_url

def get_credentials_from_env():
    """Get credentials from environment variables (for GitHub Actions)"""
    
    # In GitHub Actions, you would set these as secrets
    client_id = os.getenv('YOUTUBE_CLIENT_ID')
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    # Create credentials from refresh token
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Refresh to get access token
    creds.refresh(Request())
    
    return creds