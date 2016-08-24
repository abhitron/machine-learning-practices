import time
import tweepy
from tweepy import OAuthHandler
from tweepy import API

WEEKDAYS={0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}

##Create a twitter account if you do not already have one.
##Go to https://apps.twitter.com/ and log in with your twitter credentials.
##Click "Create New App"
##Fill out the form, agree to the terms, and click "Create your Twitter application"
##In the next page, click on "API keys" tab, and copy your "API key" and "API secret".
##Scroll down and click "Create my access token", and copy your "Access token" and "Access token secret"

api_key='YOUR_API_KEY'   #consume/api key value
api_secret='YOUR_API_SECRET' #consumer secret/api secret value
access_token='YOUR_ACCESS_TOKEN' 
access_token_secret='YOUR_ACCESS_TOKEN_SECRET'

auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = API(auth,wait_on_rate_limit=True)      #with wait_on_rate_limit set it will go on fetching all followers of user otherwise it will terminate after processing around 18k followers


def follower_generator(user_name):
    ids=[]
    for block in tweepy.Cursor(api.followers_ids,user_name).items():
        if(len(ids)<100):
            ids.append(block)
        else:
            yield ids
            ids=[]

def processing(user_name):

    time_hash={}

    for follower_ids in follower_generator(user_name):
        for user in api.lookup_users(follower_ids):
            if hasattr(user, 'status'):
                time_hash.setdefault(user.status.created_at.weekday(),{})
                time_hash[user.status.created_at.weekday()].setdefault(user.status.created_at.hour,0)
                time_hash[user.status.created_at.weekday()][user.status.created_at.hour]+=1

    result={}
    
    for key in time_hash.keys():
        max_follower_active=float('-Inf')
        result.setdefault(WEEKDAYS[key],0)
        for hour,num_follower_active in time_hash[key].iteritems():
            if(num_follower_active>max_follower_active):
                result[WEEKDAYS[key]]=hour
                max_follower_active=num_follower_active


    
    return result
