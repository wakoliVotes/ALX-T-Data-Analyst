#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# ## Table of Contents (TOC)
# 
# 1. [Data Gathering](#data-gathering)
# 2. [Assessing Data](#assessing-data)
# 3. [Identification and Listing Issues](#issues)
# 
#     3.1 [Quality Issues](#quality)
#     
#     3.2 [Tidinness Issues](#tidiness)   
# 4. [Data Cleaning](#cleaning)
# 
#     4.1 [Issue 1](#one)
#     
#     4.2 [Issue 2](#two)
#     
#     4.3 [Issue 3](#three)
#     
#     4.4 [Issue 4](#four)
#     
#     4.5 [Issue 5](#five)
#     
#     4.6 [Issue 6](#six)
#     
#     4.7 [Issue 7](#seven)
#     
#     4.8 [Issue 8](#eight)
#     
#     4.9 [Issue 9](#nine)
#     
#     4.10 [Issue 10](#ten)    
# 5. [Storing Data](#storing)
# 6. [Insights and Visualization](#analysis)
#     
#     6.1 [Insights](#insights)
#     
#     6.2 [Visualizations](#visuals)
# 7. [Reference](#ref)

# ## Data Gathering
# <a id="data-gathering"></a>
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[1]:


# Importing appropriate modules/packages

import pandas as pd
import numpy as np
import tweepy
import json
import requests
import seaborn as sb
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv(r"C:\Users\User\Documents\Udacity\Project II\twitter-archive-enhanced.csv")
# Displaying the first 5 rows
df.sample(3)


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[3]:


url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'


# In[4]:


r = requests.get(url, auth=('user', 'pass'))
r.status_code


# In[5]:


r.headers['content-type']


# In[6]:


r.encoding


# In[7]:


# Using Python's with open method in opening the file
#  the "wb" mode opens the file in binary format for writing
with open('image_predictions.tsv', 'wb') as data_file:
    data_file.write(r.content)


# In[9]:


# Reading the image predictions file and saving the data as a variable
df_image_predictions = pd.read_csv('image_predictions.tsv', sep='\t')

# Viewing part of the data, sample of 10 random rows
df_image_predictions.sample(10)


# 3. Use the Tweepy library to query additional data via the Twitter API (tweet_json.txt)

# In[10]:


# Using the available twitter information we have
# First, importing tweepy
import tweepy

consumer_key = 'KEY'
consumer_secret = 'KEY'
access_token = 'KEY'
access_secret = 'KEY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)


# In[11]:


for tweet_id in df['tweet_id']:
    try:
        tweet = api.get_status(tweet_id, tweet_mode = 'extended')
        with open('tweet_json.txt', 'a+') as file:
            json.dump(tweet._json, file)
            file.write('\n')
        print ("for id ", tweet_id, 'Success')
    except:
        print ("for id ", tweet_id, 'Failure')


# In[12]:


# Here, now saving the data in tweet_json
tweet_json = []
with open('tweet_json.txt', 'r') as file:
    content = file.readlines()
    for i in range(len(content)):
        tweet = []
        # now appending contents as found in the dataset, i.e., id, retweet_count, favorite_count and is_quote_status
        tweet.append(json.loads(content[i])['id'])
        tweet.append(json.loads(content[i])['retweet_count'])
        tweet.append(json.loads(content[i])['favorite_count'])
        tweet.append(json.loads(content[i])['is_quote_status'])

        # Merging tweet_json with tweet dataframe
        tweet_json.append(tweet)


# In[15]:


# Saving in dataframe, which will be used in subsequent analysis
# For consistency, "id" is changed to "tweet_id", which is also same in twitter_acrhive data
dataframe_column_names = ['tweet_id', 'retweet_count', 'favorite_count', 'is_quote_status']
tweet_json = pd.DataFrame(tweet_json, columns = dataframe_column_names)


# ## Assessing Data
# <a id="assessing-data"></a>
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# In[16]:


# Using describe to get an overview of the dataframe and its variable's descriptrive statistics
df.describe()


# In[17]:


df.info()


# In[18]:


# checking for posible duplicates
df.duplicated().sum()


# ## Checking the df_image_predictions dataframe

# In[19]:


df_image_predictions.info()


# In[20]:


# checking for posible duplicates
df_image_predictions.duplicated().sum()


# In[21]:


# Using describe to examine descriptive statistics for the dataframe
df_image_predictions.describe()


# In[22]:


# Checking if there are any duplicate ids in the tweets recorded
df_image_predictions['tweet_id'].duplicated().sum()


# ### Examining the tweet_json dataframe

# In[23]:


tweet_json.info()


# In[24]:


tweet_json.describe()


# In[26]:


tweet_json.duplicated().sum()


# In[27]:


tweet_json.isnull().sum()


# ## Identification and Listing of Issues: Quality & Tidiness
# <a id="issues"></a>

# ### Quality issues
# 
# 1. The source for the Tweets are too long, which can be grouped into three main areas for clarity and analysis
# 
# 2. Not all tweets have images, i,e., expanded_url's in them, and for consistency, this can be removed for respective dogs.
# 
# 3. Mix ups in representing NaN values, with some rows indicated as "None" and others using the word "NaN"
# 
# 4. Varying rating numerators in the dataframe. For consistency, this can be changed to be uniform for the numerator dog values
# 
# 5. In image descriptions, some names have underscores likely confusing, e.g., "Rhodesian_ridgeback" for "Rhodesian ridgeback"
# 
# 6. Time stamp challenges, in that it is represented both as date and clock times on same column
# 
# 7. Different irrelevant or non-clear names for the doggs, e.g., "a", "an" and "the" for a dog names is not very clear
# 
# 8. Inconsistencies in image_predictions with uppper and lowercases, e.g., beagle => Beagle, malamute => Malamute, chow ==> Chow

# ### Tidiness issues
# 
# 1. Dog types/levels are set on their own column than being combined into one for all, i.e., doggo,floofer,pupper,puppo
# 2. Merging of the data, i.e., upon cleaning, it is necessary to have one file with all the cleaned data sets

# ## Cleaning Data
# <a id="cleaning"></a>
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# In[30]:


# Make copies of original pieces of data
# Copy of twitter_archive_df
twitter_archive_copy = df.copy()

# Copy of tweet_json_df
tweet_json_copy = tweet_json.copy()

# Copy of image_predictions
image_predictions_copy = df_image_predictions.copy()


# ## Quality Issues

# ### Issue #1: Adjusting Tweet's Sources
# <a id="one"></a>

# #### Define: Readjusting Tweet Sources into Three (3) Groupings, i.e., "Twitter for iPhone", "Vine - Make a Scene" and "TweetDeck"

# #### Code

# In[31]:


# As shown below, there are four (4) core sources
twitter_archive_copy['source'].value_counts()


# In[32]:


# Replacing the source naming with simpler information,
# That is, Twitter for iPhone, TweetDeck, Twitter Wen Client and Vine - Make a Scenario

twitter_archive_copy['source'] = twitter_archive_copy['source'].str.replace('<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'Twitter for iPhone')
twitter_archive_copy['source'] = twitter_archive_copy['source'].str.replace('<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'Twitter Web Client')
twitter_archive_copy['source'] = twitter_archive_copy['source'].str.replace('<a href="http://vine.co" rel="nofollow">Vine - Make a Scene</a>', 'Vine - Make a Scene')
twitter_archive_copy['source'] = twitter_archive_copy['source'].str.replace('<a href="https://about.twitter.com/products/tweetdeck" rel="nofollow">TweetDeck</a>', 'TweetDeck')


# #### Test

# In[33]:


# Checking 'source' using .value_counts() method
twitter_archive_copy['source'].value_counts()


# In[19]:


sb.countplot(data = twitter_archive_copy, x = 'source');


# ### Issue #2: Dropping Tweets without images, i.e., expanded URLS
# <a id="two"></a>

# #### Define: In this section, the goal is using Python to drop Tweets without expanded URLs for uniformity in the dataframe

# #### Code

# In[34]:


# Checking their scope using value_counts() method
twitter_archive_copy['expanded_urls'].value_counts().sum()


# In[35]:


# Checking the total number of rows without expanded_urls
twitter_archive_copy['expanded_urls'].isnull().sum()


# - As shown from above, only 59 rows have no expanded_urls
# - This can be dropped for consistency

# In[36]:


twitter_archive_copy['expanded_urls'].dropna(inplace=True)
twitter_archive_copy.head()


# In[37]:


twitter_archive_copy = twitter_archive_copy[~twitter_archive_copy['expanded_urls'].isnull()]


# #### Test

# In[38]:


# Checking if the expanded_urls, i.e., the 59 are in the new cleaned dataframe
# As shown in the table below, nothing is returned based on .isnull() method
twitter_archive_copy[twitter_archive_copy['expanded_urls'].isnull()]


# In[39]:


# If we check counts, it is now zero(0)
twitter_archive_copy['expanded_urls'].isnull().sum()


# ### Issue 3: Mix up in representing NaN values for some rows and others "None" "NaN"
# <a id="three"></a>

# ### Define

# - In the dataset, there are sections where NaN is used while others have None
# - For consistency, all the NaN items in the dataframe can be replaced with "None"

# #### Code

# In[40]:


twitter_archive_copy.replace(np.NaN, "None", inplace=True)


# - As shown from above, for any None, there is replacing them with NaN

# #### Test

# In[41]:


# Getting a sample of the data to see the changes
twitter_archive_copy.sample(3)


# ### Issue #4: Adjusting Rating in Numerator for Consistency in the Dataset
# <a id="four"></a>

# #### Define

# The goal is realizing consistency in the dataset, which can be attained by changing the ratings to ten (10), which is the most common rating value

# #### Code

# In[42]:


# Finding the number of ratings for all the data
twitter_archive_copy.info()


# #### Ratings for Numerator

# In[43]:


# Finding the number of ratings for all the data
twitter_archive_copy['rating_numerator'].value_counts()


# - As shown above, some ratings are 13, 12, 9, 8, 7, 6, and 5

# In[44]:


# Finding the number of ratings for numerator that are not 10 (!10)
twitter_archive_copy[twitter_archive_copy['rating_numerator'] != 10]


# - The code above shows that 1842 rows have a rating that is not 10 (!10)

# In[45]:


# Identifying and recording the indexes of all rating numerator not equal to 10 using the query method
none_10_rating_numerator = twitter_archive_copy.query("rating_numerator != 10")['rating_numerator'].index


# In[46]:


# Changing the rating numerators from other values to 10
for index in none_10_rating_numerator:
    twitter_archive_copy.at[index,'rating_numerator'] = 10


# #### Test

# In[47]:


# Using the previous method, to now check the proportion of rows with none-10 as the numerator
twitter_archive_copy[twitter_archive_copy['rating_numerator'] != 10]


# - As shown above, the result brings an empty dataframe where columns now have no values
# - We can recheck the result by using the value_counts() method to know how many of the rows have 10 as the rating
# - The response should show all the rows in the dataframe, i.e., 2297, which means now all rows have a 10 as the rating

# In[48]:


# Finding the number of counts for each of the ratings in the dataframe
twitter_archive_copy['rating_numerator'].value_counts()


# #### Test

# In[49]:


# Using the previous method, to now check the proportion of rows with none-10 as the numerator
twitter_archive_copy[twitter_archive_copy['rating_numerator'] != 10]


# ### Issue # 5: Removing Underscores for names in image descriptions
# <a id="five"></a>

# #### Define:

# - As part of the identified issues, some names have underscores likely confusing
# - For example, "Rhodesian_ridgeback" for "Rhodesian ridgeback" hence a need to remove these for consistency

# #### Code

# In[50]:


# Overview of the dataset
image_predictions_copy.sample(5)


# In[51]:


# Replacing Underscores in the dataset
p1_names = image_predictions_copy['p1'].values
p2_names = image_predictions_copy['p2'].values
p3_names = image_predictions_copy['p3'].values
for x in p1_names:
    image_predictions_copy['p1'] = image_predictions_copy['p1'].str.replace("_", " ")


# In[52]:


for x in p2_names:
    image_predictions_copy['p2'] = image_predictions_copy['p2'].str.replace("_", " ")


# In[53]:


for x in p3_names:
    image_predictions_copy['p3'] = image_predictions_copy['p3'].str.replace("_", " ")


# #### Test

# In[65]:


# Using assert
assert '_' not in image_predictions_copy


# > Asserrt gives no response for the above

# In[66]:


# Sampling the data
image_predictions_copy.sample(5)


# ### Issue # 6: Time stamp challenges, in that it is represented both as date and clock times on same column
# <a id="six"></a>

# #### Define

# - This section focuses on aligning the timestamp column, so that there is consistency in the recorded timeline
# - Changing the timestamp column to be represented as datetime for consistency

# #### Code

# In[67]:


# Checking the timestamp column for processing
twitter_archive_copy['timestamp']


# In[68]:


# As shown above, timestamp is of object datatype, and we can change it to datetime
# Converting the current timestamp column to effectively have a datetime format for better quality
# Here, we use the pandas to_datetime() method

twitter_archive_copy['timestamp'] = pd.to_datetime(twitter_archive_copy['timestamp'])


# ### Test

# In[70]:


# Getting an overview of the whole dataframe, to see the new timestamp column with new datatime format
# A random sample of 10 is chosen for overview
twitter_archive_copy['timestamp'].sample(5)


# ### Issue 7: Name inconsistencies across the dog name column in twitter_archive dataset
# <a id="seven"></a>

# ### Define

# - In the name column, there are some irrelevant or non-clear names for the dogs, e.g., "a", "an" and "the", etc.
# 
# - As a means in improving the dataframe's quality, adjusting this information is useful for subsequent analysis

# #### Code

# In[71]:


# Checking the name column and listing some of its contents for better assessment
# The below list shows some names, and others which are hard to understand
twitter_archive_copy['name']


# In[72]:


# Using for loop, we can list the dog names, and check those that are suspicious as shown below
for x in twitter_archive_copy['name']:
    print(x)


# - From above, we can document a list of names which look suspecious or not informative
# - Based on personal judgment as a data analyst by looking at the sample, the below names are not clear
# - From the dataset, it is noticeable that most of the suspicious names were in lower-case, except "None"
# - Hence, listing all lowercase names can help identify the poor names for the dogs

# In[73]:


twitter_archive_copy[twitter_archive_copy.name.str.islower()].name.value_counts()


# In[74]:


# Saving the above in a list
unclear_name_list = twitter_archive_copy[twitter_archive_copy.name.str.islower()].name.values


# In[75]:


unclear_name_list


# In[76]:


# Adding NaN to the end of the list
unclear_name_list = np.append(unclear_name_list, np.NaN)
unclear_name_list


# In[77]:


# Adding "None" to the end of the list
unclear_name_list = np.append(unclear_name_list, "None")
unclear_name_list


# In[78]:


# Next, for any of the listed names above, the best option can be replacing the names with a common understandable name
# In this case, all unclear names will be replaced with "Unspecified Dog"
# The code below can be used to replace the 14 unclear names with "Unspecified Dog" using replace
# Using for loop, and the list of unclear names, we can replace in the name column as below with "Unspecified Dog"
for x in unclear_name_list:
    twitter_archive_copy['name'].replace(x, 'Dog Unknown', inplace = True)


# - The Python code above iterates through the name column, replacing all names in the unclear list

# #### Test

# In[79]:


# Using value counts to get an overview of each dog's name
twitter_archive_copy['name'].value_counts()


# In[80]:


# Running code to check the list of names in the dataframe
twitter_archive_copy['name'].sample(10)


# - As shown from above, none of the listed suspicious names can be seen in the new dataframe

# ### Issue 8 Inconsistencies in image_predictions names with uppper and lowercases
# <a id="eight"></a>

# #### Define

# - For consistency, writing the predictions with proper case is needed for quality
# - For example, in the p1, p2, and p3 columns, there are inconsistencies
# - Examples includes beagle => Beagle, malamute => Malamute, chow ==> Chow
# - Also, some names which underscores were removed as part of Issue # 5 can also be written in Capital Case

# #### Code

# In[81]:


# Rewriting the p1, p2, and p3 columns dog names into capital for each word
# First, saving the p1, p2 and p3 values in a list

p1_names = image_predictions_copy['p1'].values
p2_names = image_predictions_copy['p2'].values
p3_names = image_predictions_copy['p3'].values
# p1
# using for loop to change to upper case using title() method
for name in p1_names:
    if name.islower():
        image_predictions_copy['p1'] = image_predictions_copy['p1'].str.title()


# In[82]:


# p2
for name in p2_names:
    if name.islower():
        image_predictions_copy['p2']= image_predictions_copy['p2'].str.title()


# In[83]:


# p3
for name in p3_names:
    if name.islower():
        image_predictions_copy['p3']= image_predictions_copy['p3'].str.title()


# #### Test

# In[84]:


# Checking the new data frame
image_predictions_copy.p1


# In[85]:


image_predictions_copy.p2


# In[86]:


image_predictions_copy.p3


# ## Tidiness Issues

# In[125]:


# Saving data to manipulate
twitter_cleaned = twitter_archive_copy.copy()


# ### Issue 1: Agglomerating dog tyoes of "doggo", "floofer", "pupper" & "puppo" into a single column
# <a id="ten"></a>

# #### Define

# - In the archive dataset, the "doggo", "floofer", "pupper" & "puppo" can be merged into a single column for better presentation

# #### Code

# In[126]:


twitter_cleaned.head()


# In[ ]:


# Taking all the "doggo", "floofer", "pupper" & "puppo" and storing them into one column called "dog_phase" aspect


# In[127]:


# Making a copy of the cleaned twitter archive dataset
twitter_archive_combined = twitter_cleaned.copy()


# In[128]:


twitter_archive_combined['dog_types'] = twitter_archive_combined[['pupper','doggo', 'floofer', 'puppo']].apply(lambda x: ', '.join(x), axis=1)


# In[129]:


# Overview of joined dataset
twitter_archive_combined


# In[130]:


# Dropping the doggo floofer, pupper, puppo columns


# In[131]:


drop_columns = ['doggo' ,'floofer', 'pupper', 'puppo']
twitter_archive_combined.drop(columns= drop_columns, inplace=True)


# In[132]:


# Removing all None in the dog_types
twitter_archive_combined = twitter_archive_combined.replace(regex=r'(None,? ?)', value='').replace(regex=r'(, $)', value='')


# In[133]:


# Replacing empty occurences with NaN
twitter_archive_combined = twitter_archive_combined.replace(regex=r'', value= np.nan)


# ### Test

# In[134]:


# Counting the proportion of dog types using .value_counts() method
twitter_archive_combined['dog_types'].value_counts()


# ### Issue 2: Merging of Data into a Single Table for Tidiness
# <a id="eleven"></a>

# In[135]:


# In image predictions and twitter archive data, the tweet+ids are same, and hence the data can be merged


# In[136]:


image_predictions_copy['tweet_id']


# In[137]:


twitter_archive_combined['tweet_id']


# In[142]:


# First, merging tweet_json_copy and image_predictions_copy since inner takes two dataframes
new_clean_df = pd.merge(tweet_json_copy, image_predictions_copy,
                            on='tweet_id', how='inner')


# In[143]:


# Next, mergin the above with twitter_archive_combined
final_merged_df = pd.merge(new_clean_df, twitter_archive_combined,
                            on='tweet_id', how='inner')


# In[144]:


final_merged_df.sample(3)


# In[145]:


# Checking columns
final_merged_df.columns


# ## Storing Data
# <a id="storing"></a>
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[146]:


# Storing to master with name "twitter_archive_master.csv"
final_merged_df.to_csv('twitter_archive_master.csv', index=False)


# ## Analyzing and Visualizing Data
# <a id="analysis"></a>
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# ### Insights:
# <a id="insights"></a>
# 1. The proportion of dogs based on the three (3) sources, i.e., "Twitter for iPhone", "Vine - Make a Scene" and "TweetDeck"
# 
# 2. Proportion of dog types and their numbers in the twitter archive dataset
# 
# 3. Proportional difference in correct dog identification (True) and wrong dog identification (False) in image predictions

# #### Code

# In[147]:


# First, reading the master dataset for use in the analysis
master_dataset = pd.read_csv('twitter_archive_master.csv')


# In[148]:


# twitter_archive_copy dataframe
#  1. The proportion of dogs based on the three (3) sources
#  i.e., "Twitter for iPhone", "Vine - Make a Scene" and "TweetDeck"
master_dataset['source'].value_counts()


# In[149]:


# Percentages
sources = master_dataset['source'].value_counts() / len (master_dataset['source']) * 100
sources


# - Of all sources, Twitter for iPhone has the most (94.17%), followed by Vine - Make a Scene (3.96%), Twitter Web Client (1.39%), then TweetDeck (0.48%) as the last

# #### 2. Proportion of dog breeads and their numbers in the image predictions dataset

# In[150]:


master_dataset['dog_types'].value_counts()


# - As shown rom above, the most dog stage is Pupper 211, Doggo 67, and Puppo 23. Specifically Floofer are 7
# - Other dog types were mixed, based on similar traits

# In[151]:


# Percentage proportions
dog_type_list = master_dataset['dog_types'].value_counts() / len (master_dataset['dog_types']) * 100
dog_type_list


# ##### - 3. Correct dog identification (True) and wrong dog identification (False) for p1_dog, p2_dog and p3_dog

# In[152]:


image_predictions_copy[image_predictions_copy['p1_dog'] == True].value_counts().sum() / len(image_predictions_copy['p1_dog']) * 100


# In[153]:


image_predictions_copy[image_predictions_copy['p2_dog'] == True].value_counts().sum() / len(image_predictions_copy['p2_dog']) * 100


# In[154]:


image_predictions_copy[image_predictions_copy['p3_dog'] == True].value_counts().sum() / len(image_predictions_copy['p3_dog']) * 100


# - From above, of all the identified dogs, 73.83%, 74.84% and 72.24% were correct for p1_dog, p2_dog and p3_dog respectively

# ### Visualization
# <a id="visuals"></a>

# In[155]:


# Graphically representing Corectly Identified Dogs vs Falsely Identified Dogs
# This visualization is for p1_dog
p1_values = master_dataset['p1_dog'].value_counts(normalize=True).values * 100
dog_identification  = ['Correctly Identified-True','Wrongly Identified-False']


# In[156]:


fig = plt.figure(figsize = (10, 6))

plt.bar(dog_identification, p1_values,color='green',width= 0.8)
plt.xlabel('Dog Identification - True vs. False',fontsize=18)
plt.ylabel('Percentage',fontsize=20)
plt.title('Percentage of Correct vs. Wrong Identified Dogs', fontsize=22)
plt.show()


# In[157]:


master_dataset['source'].value_counts()


# In[158]:


sources = master_dataset['source'].value_counts() / len (master_dataset['source']) * 100
sources


# - In the merged dataset, it shows Twitter for iPhone as the most source with 98%, accounting for 2034 of the tweet_ids 

# In[159]:


fig = plt.figure(figsize = (10, 6))
source_types = ("Twitter for iPhone", "Vine - Make a Scene", "TweetDeck")

plt.bar(source_types, sources, color='blue',width= 0.8)
plt.xlabel('Source Type',fontsize=18)
plt.ylabel('Percentage',fontsize=20)
plt.title('Percentage of Tweet Sources on 4 Types', fontsize=22)
plt.show()


# - From above, it visually seen that most of the tweets are for the source "Twitter for iPhone" with 98%

# ### References
# <a id="ref"></a>"
# 1. Python Community (2022). [requests 2.28.1](https://pypi.org/project/requests/)
