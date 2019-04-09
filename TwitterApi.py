import tweepy

class TwitterScrape():

    def __init__(self, numPosts, twitterUser):
        self.numPosts = numPosts
        self.twitterUser = twitterUser

    def grabRecentPosts(self):
        #Initialize the API with the access tokens
        auth = tweepy.OAuthHandler('HGdiUJC4v1zrYkleCp2Q90HaJ', 'N6O8NeMe7iLJVYhmaEpAX2RILQx1TVORGnZ7STqdapW4AqvlLI')
        auth.set_access_token('1091938307930492928-6hKXJkMQJm3BkzGGk2VakRGVgu1DtO', 'iFXOmEDTd9vCMQlN4ZxbUWMfX6vYBPrQkIWPtOe9VAi72')
        api = tweepy.API(auth)
        
        #set the user to the username given in the parameters
        tweets = api.user_timeline(screen_name = self.twitterUser, count = self.numPosts)

        #return the dictionary
        return tweets

tweet = TwitterScrape(5, 'graem_timmons')
tweets = tweet.grabRecentPosts()

for statuses in tweets:
    print(statuses.text)