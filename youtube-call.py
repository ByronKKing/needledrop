
from apiclient.discovery import build

api_key = "AIzaSyBJDC-qDsI7OAE52U-j-tfEqgFFNMZELBE"

youtube = build('youtube', 'v3', developerKey=api_key)

channels_response = youtube.channels().list(
  part="contentDetails",
  forUsername="theneedledrop"
).execute()

uploadId = channels_response['items'][0]['id']

print(uploadId)

playlistitems_list_request = youtube.playlistItems().list(
playlistId=uploadId,
part="snippet",
maxResults=50
)

print(playlistitems_list_request)

