# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 22:10:03 2019

@author: Sarthak
"""

import re
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler

class TwitterClient(object):
    
    def __init__(self):
        
        ck='VAB783khHiAX1hDMwmoeEoUPH' 
        csk='vVriQ1bxRo50xtWtB4vw6q5O3ihiIu2HBpRQtcFU5SCARuUZM2' 
        atk='3228432704-tNilRZxhI5C7mDdOi0HffWmp3jm9ImdF2AgcdgY' 
        atsk='RNzXwB3hlUCbCYlNFfFJnXxpXkEAaS2WToTMhwcIFbiH1' 
        
        try:
            self.auth = OAuthHandler(ck, csk)
            self.auth.set_access_token(atk, atsk) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
            
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet) 
   
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        '''if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  '''
        return analysis.sentiment.polarity
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q=query,count=count) #since="2014-01-01",
                           #until="2014-02-01"
            
            for tweet in fetched_tweets: 
                
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                if parsed_tweet['sentiment']==0:
                    print(parsed_tweet['text'])
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # retweeet
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main():
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query="#kesari",count=500) 
     # picking positive tweets from tweets 
    npt=0
    senttweet=[tweet['sentiment'] for tweet in tweets if tweet['sentiment']>=0]
    npt=len(senttweet)
    print(npt)
    finalsent=npt/len(tweets)
    print(finalsent)
    import pandas as pd
    import numpy as np
    data=pd.read_excel("film.xlsx")
    data=data.replace([r"\bpoor\b",r"\baverage\b",r"\bgood\b"],[0.33,0.66,0.99],regex=True)

    x=data.drop(["revenue","name"],axis=1)
    y=data["revenue"]

    from sklearn.linear_model import LinearRegression
    lrm=LinearRegression()
    lrm.fit(x,y)
    finalsent*=5
    m=np.array([finalsent,0.99,0.66])
    M=m.reshape(1,-1)
    r=lrm.predict(M)
    print(r)

if __name__ == "__main__":
     main()