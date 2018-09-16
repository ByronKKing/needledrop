# The Needledrop

This is an analysis I put together on Anthony Fantano's music reviewing Youtube channel, The Needledrop. I was looking for an excuse to use the Youtube API, which is very easy to use and gives access to a lot of interesting datapoints on published videos. 

I first built a python script that uses the API to gather information on all his videos. I then analyzed the videos in a jupyter notebook. Finally, I built a model to predict what score Anthony will give to new videos. He reviews a new album almost every day, so the script runs on a daily basis and predicts what score he gave to the album based on characteristics of the video, as well as information on the album itself.


## youtube-call.py

This script gathers the historical information on all of the Needledrop's videos. Some of the datapoints include how many comments, likes, dislikes, favorites and views a video has, as well as the duration of the video and the content of the description.

The content of the description is key, because I use information that Anthony always writes in the description to create variables for the album itself, such as the genre of music for the album.

## needledrop-analysis.ipynb

This jupyter notebook uses this historical data to analyze the reviewer's tendencies. I look at such descriptive stats as the average rating for each music genre, as well as the most frequent genre of music he reviews.

In this script I also put my model-building process. I use an ordinal regression model to predict, give information on the video and the album, what score he is likely to give. It comes as no surprise to anyone who reviews the channel that Anthony is likely to give an album deemed "experimental" a favorable review...

## daily-scoring.py

This python script runs on a daily basis. It calls the API, and looks to see if any of the Needledrop's recent reviews are already in the historical dataset. If not, it adds it to the dataset, and predicts the rating that Anthony gives. It then saves the score and the prediction to a csv, and sends an email once it adds the video to the dataset.

