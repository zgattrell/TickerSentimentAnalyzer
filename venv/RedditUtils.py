import praw
import pandas as pd
from textblob import TextBlob
import datetime as datetime

#Will return a dataframe of the posts searching for the ticker and company name
#arg1=subreddit arg2=Ticker 1 arg3=Search item 2
def getDataframe(arg1, arg2, arg3):
    df = getPost(arg1, arg2, arg2).append(getPost(arg1, arg2, arg3))
    return df
#takes a subreddit and returns a dataframe of companies and the current sentiment
#arg1=subreddit arg2=ticker item arg3=search item
def getPost(arg1, arg2, arg3):
    #initialize the reddit client with credentials
    reddit = praw.Reddit(client_id='CLIENT_ID', client_secret='CLIENT_SECRET',
                         user_agent='MemeScraper1.0')
    #select the subreddit we are going to be scanning through
    subreddit = reddit.subreddit(arg1)
    #create a dataframe for holding the data. ID given from reddit | # of interactions with the post/# of comments on post | overall sentiment of post and comments
    df = pd.DataFrame(columns=['Post_ID','Time_Created','Ticker','Post_Title','Post_Comments','Overall_Post_Sentiment'])
    #iterate through the subreddit looking for posts containing the keywords
    for submission in subreddit.search(arg3, limit=10):
        row = {'Post_ID':submission.id,'Time_Created':datetime.datetime.fromtimestamp(submission.created_utc).date(),'Ticker':arg2,'Post_Title':submission.title,'Post_Comments':submission.num_comments,'Overall_Post_Sentiment':getPostSentiment(submission)}
        df = df.append(row, ignore_index=True)
    return df
    #print(df.to_string())

def getPostSentiment(arg1):
    submission = arg1
    post_Sentiment = 0;
    post_Sentiment += TextBlob(submission.title).sentiment.polarity * TextBlob(submission.title).sentiment.subjectivity
    for comment in submission.comments:
        post_Sentiment += TextBlob(comment.body).sentiment.polarity * TextBlob(comment.body).sentiment.subjectivity
    return post_Sentiment


