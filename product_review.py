# -*- coding: utf-8 -*-
"""product_review

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1spwtugjUSnkvo38FtyvaNOzOAbeT1Lp9
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
import csv

# List of URLS to search
list_of_urls = ['https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_arp_d_viewopt_rvwer?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=1',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=2',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=3',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=4',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=5',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=6',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=7',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=8',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=9',
                'https://www.amazon.com/Assault-Fitness-Air-Bike-AirBike/product-reviews/B00F74RX40/ref=cm_cr_getr_d_paging_btm_next_7?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=10']

# Retrieve each of the url's HTML data and convert the data into a beautiful soup object.
# Find, extract and store reviewer names and review text into a list.

names = []
reviews = []
data_string = ""

for url in list_of_urls:
    params = {'api_key': "ENTERAPIKEYHERE", 'url': url}
    response = requests.get('http://api.scraperapi.com/',   params=urlencode(params))
    soup = BeautifulSoup(response.text, 'html.parser')

    for item in soup.find_all("span", class_="a-profile-name"):
      data_string = data_string + item.get_text()
      names.append(data_string)
      data_string = ""

    for item in soup.find_all("span", {"data-hook": "review-body"}):
      data_string = data_string + item.get_text()
      reviews.append(data_string)
      data_string = ""

# Create the dictionary
reviews_dict = {'Reviewer Name': names, 'Reviews': reviews}

# Print the lengths of each list.
print(len(names), len(reviews))

# Create a new dataframe
df = pd.DataFrame.from_dict(reviews_dict, orient='index')
df.head()

# Delete all the columns that have missing values
df.dropna(axis=1, inplace=True)
df.head()

# Transpose the dataframe
prod_reviews = df.T
print(prod_reviews.head(10))

# Remove special characters
prod_reviews['Reviews'] = prod_reviews['Reviews'].str.replace('\n','')
prod_reviews.head(5)

# Convert dataframe to CSV file
prod_reviews.to_csv('reviews.csv', index=False, header=True)

"""# Sentiment Analysis"""

import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

data = pd.read_csv('/content/rogue_reviews.csv')
data.head()

data.info()

# drop any null values

data.dropna(inplace=True)

nltk.download('wordnet')

# polarity and subjectivity using wordnet and textblob based on review text
# 1 = positive
# -1 = negative
from textblob import TextBlob

# Lambda function to find the polarity of each review
data['Reviews']= data['Reviews'].astype(str)
pol = lambda x: TextBlob(x).sentiment.polarity
data['polarity'] = data['Reviews'].apply(pol)

# Plot of scores
import matplotlib.pyplot as plt
import seaborn as sns
num_bins = 50
plt.figure(figsize=(10,6))
n, bins, patches = plt.hist(data.polarity, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Polarity')
plt.ylabel('Number of Reviews')
plt.title('Histogram of Polarity Score')
plt.show();

stp_words=stopwords.words('english')
def clean_review(review):
  cleanreview=" ".join(word for word in review.
                       split() if word not in stp_words)
  return cleanreview

data['Reviews']=data['Reviews'].apply(clean_review)

data.head()

data['polarity'].value_counts()

# neutral review word cloud - polarity score equal to "0"

from wordcloud import WordCloud

consolidated=' '.join(word for word in data['Reviews'][data['polarity']==0].astype(str))
wordCloud=WordCloud(width=1600,height=800,random_state=21,max_font_size=110)
plt.figure(figsize=(15,10))
plt.imshow(wordCloud.generate(consolidated),interpolation='bilinear')
plt.axis('off')
plt.show()

# positive review word cloud - polarity score equal to "1"

consolidated=' '.join(word for word in data['Reviews'][data['polarity']==1].astype(str))
wordCloud=WordCloud(width=1600,height=800,random_state=21,max_font_size=110)
plt.figure(figsize=(15,10))
plt.imshow(wordCloud.generate(consolidated),interpolation='bilinear')
plt.axis('off')
plt.show()

# word cloud - reviews greater than 0 (positive)

consolidated=' '.join(word for word in data['Reviews'][data['polarity']>=0].astype(str))
wordCloud=WordCloud(width=1600,height=800,random_state=21,max_font_size=110)
plt.figure(figsize=(15,10))
plt.imshow(wordCloud.generate(consolidated),interpolation='bilinear')
plt.axis('off')
plt.show()

# negative reviews - polarity scores less than "0"

consolidated=' '.join(word for word in data['Reviews'][data['polarity']<0].astype(str))
wordCloud=WordCloud(width=1600,height=800,random_state=21,max_font_size=110)
plt.figure(figsize=(15,10))
plt.imshow(wordCloud.generate(consolidated),interpolation='bilinear')
plt.axis('off')
plt.show()