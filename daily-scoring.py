
from apiclient.discovery import build
import pandas as pd
import smtplib
from sklearn.externals import joblib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(subject,body):
    msg = MIMEMultipart()
    msg['From']="aspidistraflyer@yahoo.com"
    msg['To']="byronkking@gmail.com"
    msg['Subject']=subject
    body = bodya
    body = MIMEText(body)
    msg.attach(body)

    s = smtplib.SMTP(host="smtp.mail.yahoo.com", port=587)
    s.starttls()
    s.login("aspidistraflyer@yahoo.com", "tojestmojhaslo")
    s.sendmail("byronkking@gmail.com","aspidistraflyer@yahoo.com",msg)
    s.quit()


###call api for last 50 vids

api_key = APIKEY
youtube = build('youtube', 'v3', developerKey=api_key)

channels_response = youtube.channels().list(
  part="contentDetails",
  forUsername="theneedledrop"
).execute()

playlistId = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

vidList = youtube.playlistItems().list(
playlistId=playlistId,
part="snippet",
maxResults=50
).execute()

vidIds = vidList['items']

vidIdList = []
for vid in vidIds:
    vidIdList.append(vid['snippet']['resourceId']['videoId']) 

vidList = []
for i in range(0, len(vidIdList), 50):
    toappend = ','.join(map(str,vidIdList[i:i + 50]))
    vidList.append(toappend)

vids = []
for vid in vidList:
    video_response = youtube.videos().list(
        id=vid,
        part='snippet, contentDetails, statistics, recordingDetails'
    ).execute()
    vids.append(video_response)   

dictList = []
for vid in vids:
    rows = vid['items']
    for row in rows:
        currentDict = {}
        #get vid id
        currentDict['id'] = row['id']
        #snippet
        xx = row['snippet']
        currentDict['description'] = xx['description']
        currentDict['live_broadcast'] = xx['liveBroadcastContent']
        currentDict['published_at'] = xx['publishedAt']
        currentDict['tags'] = xx['tags']
        try:
            currentDict['thumbnail'] = xx['thumbnails']['standard']['url']
        except:
            currentDict['thumbnail'] = "none"
        currentDict['title'] = xx['title']
        #contentDetails
        xx = row['contentDetails']
        currentDict['duration'] = xx['duration']
        currentDict['definition'] = xx['definition']
        #recordingDetails
        try:
            xx = row['recordingDetails']['location']
            currentDict['altitude'] = xx['altitude']
            currentDict['latitude'] = xx['latitude']
            currentDict['longitude'] = xx['longitude']
        except:
            currentDict['altitude'] = None
            currentDict['latitude'] = None
            currentDict['longitude'] = None
        #statistics
        xx = row['statistics']
        currentDict['comments'] = xx['commentCount']
        currentDict['dislikes'] = xx.get('dislikeCount')
        currentDict['favorites'] = xx['favoriteCount']
        currentDict['likes'] = xx.get('likeCount')
        currentDict['views'] = xx.get('viewCount')
        dictList.append(currentDict)


###get rid of existing videos in dataset

df = pd.DataFrame(dictList)
existing = pd.read_csv("~/needledrop/raw-data.csv")

df = df[~df.countries.isin(existing.id.unique())]

if df is not None:
	existing = existing.append(df)
	existing.to_csv("~/needledrop/raw-data.csv",index=False)
else:
	sendEmail("ND Update: No New Vids","There were no new videos to add to the dataset.")
    sys.exit()


###processing

df['rating'] = None
df['rating'][df['description'].str.contains('1/10', case=False, na=False)] = 1
df['rating'][df['description'].str.contains('2/10', case=False, na=False)] = 2
df['rating'][df['description'].str.contains('3/10', case=False, na=False)] = 3
df['rating'][df['description'].str.contains('4/10', case=False, na=False)] = 4
df['rating'][df['description'].str.contains('5/10', case=False, na=False)] = 5
df['rating'][df['description'].str.contains('6/10', case=False, na=False)] = 6
df['rating'][df['description'].str.contains('7/10', case=False, na=False)] = 7
df['rating'][df['description'].str.contains('8/10', case=False, na=False)] = 8
df['rating'][df['description'].str.contains('9/10', case=False, na=False)] = 9
df['rating'][df['description'].str.contains('10/10', case=False, na=False)] = 10

df['rating'] = pd.to_numeric(df['rating'])

def test_title(x):
    xx = x.split(' - ')
    if len(xx) > 1:
        return(xx[1])
    
df['album'] = df['title'].apply(test_title)

df['album'] = df.album.str.replace("Review","")
df['album'] = df.album.str.replace("ALBUM REVIEW","")
df['album'] = df.album.str.replace("EP REVIEW","")
df['album'] = df.album.str.replace("MIXTAPE REVIEW","")
df['album'] = df.album.str.replace("REVIEW","")
df['album'] = df.album.str.replace("QUICKIE","")
df['album'] = df.album.str.replace("ALBUM","")
df['album'] = df.album.str.replace("MIXTAPE","")
df['album'] = df.album.str.replace("COMPILATION","")
df['album'] = df.album.str.replace("TRACK","")
df[df['album'].isnull()].head()

df['artist'] = df['title'].apply(lambda x: x.split(' - ')[0])

df['electronic'] = 0
df['electronic'][df['tags'].str.contains('electronic', case=False, na=False)] = 1
df['hip_hop'] = 0
df['hip_hop'][df['tags'].str.contains('hip hop', case=False, na=False)] = 1
df['metal'] = 0
df['metal'][df['tags'].str.contains('metal', case=False, na=False)] = 1
df['folk'] = 0
df['folk'][df['tags'].str.contains('folk', case=False, na=False)] = 1
df['indie'] = 0
df['indie'][df['tags'].str.contains('indie', case=False, na=False)] = 1
df['underground'] = 0
df['underground'][df['tags'].str.contains('underground', case=False, na=False)] = 1
df['experimental'] = 0
df['experimental'][df['tags'].str.contains('experimental', case=False, na=False)] = 1
df['instrumental'] = 0
df['instrumental'][df['tags'].str.contains('instrumental', case=False, na=False)] = 1
df['rock'] = 0
df['rock'][df['tags'].str.contains('rock', case=False, na=False)] = 1
df['rap'] = 0
df['rap'][df['tags'].str.contains('rap', case=False, na=False)] = 1
df['jazz'] = 0
df['jazz'][df['tags'].str.contains('jazz', case=False, na=False)] = 1

df['published_at'] = pd.to_datetime(df['published_at'])

df['year'] = df.published_at.dt.year
df['month'] = df.published_at.dt.month
df['dow'] = df.published_at.dt.dayofweek
df['week'] = df.published_at.dt.week

df[['year', 'month', 'dow','week']] = df[['year', 'month', 'dow','week']].apply(lambda x: x.astype('category'))
df[['electronic', 'hip_hop', 'metal','folk',
   'indie','underground','experimental',
   'instrumental','rock','rap','jazz']] = df[['electronic', 'hip_hop', 'metal','folk',
   'indie','underground','experimental',
   'instrumental','rock','rap','jazz']].apply(lambda x: x.astype('category'))
df['rating_bucket'] = df['rating'].astype('str')
df['rating_bucket'][df.rating.isin([1,2,3])] = "1-3"


###make prediction

data = df[df.rating.notnull()&df.album.notnull()&df.artist.notnull()]

if data is None:
	sendEmail("ND Update: No New Predictions","There were no new predictions to add to the dataset.")
    sys.exit()

multModel = joblib.load("multreg-weights.sav")
data['pred'] = multModel.predict(data[['comments','likes','dislikes','favorites','views',
                   'electronic','hip_hop','metal','folk','indie','underground',
                   'experimental','instrumental','rock','rap','jazz',
                   'month','year','month','dow','week']])

scores = data[['id','title','artist','album','rating_bucket','pred']]

existingscores = pd.read_csv("~/needledrop/scores.csv")

scores = scores[~scores.id.isin(existingscores.id.unique())]

if scores is not None:
	existingscores = existingscores.append(scores)
	existingscores.to_csv("~/needledrop/scores.csv",index=False)
    sendEmail("ND Update: New Scores","New scores were updated and saved.")
else:
	sendEmail("ND Update: No New Scores","The script did not save any new scores.")


