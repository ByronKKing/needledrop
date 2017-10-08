from apiclient.discovery import build
import pandas as pd

##initialize api call

api_key = APIKEY
youtube = build('youtube', 'v3', developerKey=api_key)

##get playlistId for needledrop channel

channels_response = youtube.channels().list(
  part="contentDetails",
  forUsername="theneedledrop"
).execute()

playlistId = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

##loop over all videos in channel playlist and retrieve video ids

vidList = youtube.playlistItems().list(
playlistId=uploadId,
part="snippet",
maxResults=50
).execute()

nextPageToken = vidList.get('nextPageToken')

while ('nextPageToken' in vidList):
    nextPage = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlistId,
    maxResults="50",
    pageToken=nextPageToken
    ).execute()
    vidList['items'] = vidList['items'] + nextPage['items']

    if 'nextPageToken' not in nextPage:
        vidList.pop('nextPageToken', None)
    else:
        nextPageToken = nextPage['nextPageToken']

vidIds = vidList['items']

vidIdList = []
for vid in vidIds:
    vidIdList.append(vid['snippet']['resourceId']['videoId']) 

len(vidIdList) #matches up with actual number of ND videos


##get all fields for vids in list

#create list of comma separated lists 50 elements each
vidList = []
for i in range(0, len(vidIdList), 50):
    toappend = ','.join(map(str,vidIdList[i:i + 50]))
    vidList.append(toappend)

#retrieve info for all videos, 50 at a time
vids = []
for vid in vidList:
    video_response = youtube.videos().list(
        id=vid,
        part='snippet, contentDetails, statistics, recordingDetails'
    ).execute()
    vids.append(video_response)


##retrieve relevant fields for each video and store in dataframe

dictList = []

for vid in vidList:
    currentDict = {}
    xx = vid['snippet']
    try:
        currentDict['thumbnail'] = xx['thumbnails']['standard']['url']
    except:
        currentDict['thumbnail'] = "none"
    currentDict['published_at'] = xx['publishedAt']
    currentDict['description'] = xx['description']
    currentDict['title'] = xx['title']
    currentDict['video_id'] = xx['resourceId']['videoId']
    dictList.append(currentDict)

df = pd.DataFrame(dictList)
df.head()
