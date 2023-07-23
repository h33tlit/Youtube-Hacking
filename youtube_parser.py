import googleapiclient.discovery
import googleapiclient.errors
import json
import datetime
from datetime import timedelta
import requests

# Set up the YouTube Data API client
api_service_name = "youtube"
api_version = "v3"
api_key = "<KEY>"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

def get_video_details(video_id):
    try:
        # Call the videos.list method to retrieve video details
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if 'items' in video_response and len(video_response['items']) > 0:
            video = video_response['items'][0]
            title = video['snippet']['title']
            thumbnail_url = video['snippet']['thumbnails']['high']['url']
            tags = video['snippet'].get('tags', [])
            return title, tags, thumbnail_url

        return "Not found", "Not found", None

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return "Not found", "Not found", None

def download_thumbnail(thumbnail_url, video_id):
    try:
        # Send a GET request to fetch the thumbnail image
        response = requests.get(thumbnail_url)
        response.raise_for_status()

        # Save the thumbnail image to a file
        with open(f"Thumbnails/thumbnail_{video_id}.jpg", "wb") as file:
            file.write(response.content)

        print(f"Thumbnail for video {video_id} downloaded successfully!")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading thumbnail for video {video_id}: {str(e)}")

def search_videos(query):
    try:
        ### Call the search.list method to retrieve search results
        search_response = youtube.search().list(
            q=query,
            part="id",
            maxResults=5,
            type="video"
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]
        return video_ids

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return []

# Example usage:
search_results = search_videos("hacking")

for video_id in search_results:
    title, tags, thumbnail_url = get_video_details(video_id)
    print(f"Video ID: {video_id}")
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    if thumbnail_url:
        print(f"Downloading thumbnail for video {video_id}...")
        download_thumbnail(thumbnail_url, video_id)
    else:
        print("Thumbnail not found.")
    print()