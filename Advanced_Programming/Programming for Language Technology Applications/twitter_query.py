import sys
import tweepy

#Set the authentication credentials
consumer_key = "59j7xN1pSsbhs3uc2jTwt8v2H"
consumer_secret = "F1XqnSCbt4lBjpLuIoYnGmLfMBFoUVxkUml7CMbTerA3Tk6pEw"
access_token = "35521051-KkPDOLEbZ124WH7qUkDroZA2pQGVUwKsv7zW1xRdl"
access_token_secret = "qRyp1x5m9eM4egAI8SUpZzzfm1YBMVKt4ZaG6Ah6E8Bi6"

#Instantiate the api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Create API object
api = tweepy.API(auth)


def get_tweets(profile,most_recent=None):
    try:
        if int(most_recent) > 0:
            #This method handles the tweets, retweets, statuses on your/someone else's timeline as long as the account is public
            tweets = api.user_timeline(screen_name=profile, count=int(most_recent))
            for tweet in tweets:
                print(f"{tweet.created_at}: {tweet.text}")
        elif int(most_recent) <0:
            print('Error: Pass a positive value N or none.')
        else:
            pass
    except:
        tweets = api.user_timeline(screen_name=profile, count=1)
        for tweet in tweets:
            print(f"{tweet.created_at}: {tweet.text}")

        
if len(sys.argv) == 3 : 
    get_tweets(str(sys.argv[1]),str(sys.argv[2]))
else:
    get_tweets(str(sys.argv[1]))
