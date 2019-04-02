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
        
        ck='your key' 
        csk='your key' 
        atk='your key' 
        atsk='your key'
        
        try:
            self.auth = OAuthHandler(ck, csk)
            self.auth.set_access_token(atk, atsk) 
            #Creating tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
            
    def clean_tweet(self, tweet): 
        ''' 
        Function to clean tweet text by removing links, special characters 
        using regex statements. 
        '''
        return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet) 
   
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Function to return sentiment polarity of the passed tweet 
        using textblob's sentiment attribute 
        '''
        #Calling TextBlob on passed tweet 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        #Returning polarity
        return analysis.sentiment.polarity
    
    
     def get_tweet_subjectivity(self, tweet): 
        ''' 
        Function to return sentiment subjectivity of the passed tweet 
        using textblob's sentiment method 
        '''
        #Calling TextBlob on passed tweet  
        analysis = TextBlob(self.clean_tweet(tweet)) 
        #Returning subjectivity
        return analysis.sentiment.subjectivity
    
    
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        tweets = [] 
  
        try: 
            #Calling api.search to fetch tweets 
            fetched_tweets = self.api.search(q=query,count=count) #since="2014-01-01",
                           #until="2014-02-01"
            
            for tweet in fetched_tweets: 
                
                parsed_tweet = {} 
  
                #Saving text of the tweet 
                parsed_tweet['text'] = tweet.text 
                #Saving sentiment of the tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                #Saving subjectivity of the tweet
                parsed_tweet['subjectivity']= self.get_tweet_subjectivity(tweet.text)
           
                #Appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # retweeet
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            #Returning the parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main():
    #Creating an object of TwitterClient Class 
    api = TwitterClient() 
    
    #Calling member function to get tweets based on movie name
    tweets = api.get_tweets(query="#kesari",count=500)
    
    #Picking positive tweets from tweets
    senttweet=[tweet['sentiment'] for tweet in tweets if tweet['sentiment']>=0]
    
    #Picking neutral tweets from tweets
    neutraltweets=[tweet for tweet in tweets if tweet['sentiment']==0]
    npt=len(senttweet)
    nnt=len(neutraltweets)
    print(npt)
    finalsent=npt/(len(tweets)-nnt)
    print(finalsent)
    
    #Importing the created Bollywood movie dataset
    import pandas as pd
    import numpy as np
    data=pd.read_excel("film.xlsx")
    data=data.replace([r"\bpoor\b",r"\baverage\b",r"\bgood\b"],[0.33,0.66,0.99],regex=True)
    
    #Assigning data
    x=data.drop(["revenue","name"],axis=1)
    y=data["revenue"]
    
    #Fitting the data to the model
    from sklearn.linear_model import LinearRegression
    lrm=LinearRegression()
    lrm.fit(x,y)
    
    #Preparing input
    finalsent*=5
    m=np.array([finalsent,0.99,0.66])
    M=m.reshape(1,-1)
    
    #Prediction
    r=lrm.predict(M)
    print(r)
    
#Calling the main function
if __name__ == "__main__":
     main()
