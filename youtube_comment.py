import re
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

# --- CONFIGURATION ---
# 2. Load the variables from the .env file
load_dotenv()

# 3. Access the key safely
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_video_id(url):
    """Extends a standard YouTube URL to extract the Video ID."""
    video_id_search = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return video_id_search.group(1) if video_id_search else None

def fetch_comments(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []
    
    # Initialize the request
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  # API limit per page
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments.append(f"{user}: {comment}")

        # Check if there is another page of comments
        request = youtube.commentThreads().list_next(request, response)

    return comments

def main():
    url = input("Enter YouTube Video Link: ").strip()
    video_id = get_video_id(url)

    if not video_id:
        print("Invalid YouTube URL.")
        return

    print(f"Fetching comments for video ID: {video_id}...\n")
    
    try:
        all_comments = fetch_comments(video_id)
        
        for i, comment in enumerate(all_comments, 1):
            print(f"[{i}] {comment}")
            
        print(f"\n--- Done! Total comments retrieved: {len(all_comments)} ---")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()