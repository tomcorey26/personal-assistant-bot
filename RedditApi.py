import praw

numPosts = 5



#limit = Int
#subreddit = "subreddit name"
#random = True

def redditPosts(numPosts = 5, **kwargs):
    #Initialize reddit request info
    reddit = praw.Reddit(client_id='cAABwwx3KhnYiw',
                     client_secret='y2y0kH0hQLIwaWpkGOaMlM3Rtvc',
                     user_agent='Personal Assistant1 by /u/recievebacon',
                     password='graem161',
                     username='recievebacon')

    #Case for random subreddit
    if 'random' in kwargs:
        if kwargs['random'] == True:
            sub = reddit.random_subreddit()
            print("The random subreddit is: " + sub.display_name + "\n")
            for submission in reddit.subreddit(sub.display_name).hot(limit = numPosts):
                print(submission.title)
                print(submission.url + "\n")
    #Case for default
    for submission in reddit.front.hot(limit = numPosts):
        print(submission.title)
        print(submission.url + "\n")

redditPosts(5)