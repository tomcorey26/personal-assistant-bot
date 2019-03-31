import praw

#limit = Int
#subreddit = "subreddit name"
#random = True

class RedditScrape():

    def __init__(self, numPosts, subReddit):
        self.numPosts = numPosts
        self.subReddit = subReddit

    def grabTopPosts(self, numPosts, subReddit):
        reddit = praw.Reddit(client_id='cAABwwx3KhnYiw',
                     client_secret='y2y0kH0hQLIwaWpkGOaMlM3Rtvc',
                     user_agent='Personal Assistant1 by /u/recievebacon',
                     password='graem161',
                     username='recievebacon')
        #make a dictionary for post titles and links
        posts = {}
        #Case for default
        if self.subReddit == 'all':
            for submission in reddit.front.hot(limit = self.numPosts):
                print(submission.title)
                print(submission.url + "\n")
                #add the current post to the dictionary
                posts[str(submission.title)] = submission.url
        else:
            #Case for random subreddit
            if self.subReddit == 'random':
                #set the sub to a random one
                sub = reddit.random_subreddit()
            #Case for given subreddit
            else:
                #set the sub to the one in the parameters
                sub = reddit.subReddit(self.subReddit)
            #look for the top posts
            print("Searching through " + sub.display_name + "\n")
            for submission in reddit.subreddit(sub.display_name).hot(limit = self.numPosts):
                print(submission.title)
                print(submission.url + "\n")
                #add the current post to the dictionary
                posts[str(submission.title)] = submission.url
        #return the dictionary
        return posts