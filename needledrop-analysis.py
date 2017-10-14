
# coding: utf-8

# In[51]:

import pandas as pd
import numpy as np


# In[2]:

df = pd.read_csv('~/needledrop/raw-data.csv')


# In[ ]:

#artist
#album
#genre
#album summary
#rating


# # Explore

# In[64]:

df.head()


# In[35]:

df.info()
df.dtypes


# In[36]:

df.describe()


# In[40]:

df['description'] = df['description'].astype('str')


# # Processing

# In[63]:

#get rating
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


# In[79]:

#get artist
df.iloc[1].title.split('-')[0]


# In[91]:

#get album
def test_title(x):
    xx = x.split('-')
    if len(xx) > 1:
        return(xx[1])
    
df['album'] = df['title'].apply(test_title)


# In[94]:

df['album'] = df.album.str.replace("Review","")


# In[85]:

#get artist
df['artist'] = df['title'].apply(lambda x: x.split('-')[0])

