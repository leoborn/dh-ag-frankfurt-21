# This is the Twitter library we use.
import twitter
# Since we want to report some statistics, we import FreqDist.
from nltk import FreqDist
# This library is for saving binary objects to files.
import pickle

# Initialize the Twitter library with our credentials.
api = twitter.Api(
  consumer_key='',
  consumer_secret='',
  access_token_key='',
  access_token_secret='',
  cache=None,
  # Set tweet_mode to 'extended' to get full-text tweets instead of shortened tweets.
  tweet_mode= 'extended'
)

#print(api.VerifyCredentials())

# 東京五輪 is worth a thousand tweets
#
# The actual query is formatted as a raw Twitter query.
# Here we want to get 1000 tweets containing the hashtag (== "%23") 東京五輪.
tweets = api.GetSearch(
  raw_query="q=%23東京五輪&result_type=recent&count=1000"
)

# We want to keep those that are not retweets.
original_tweets = []

# Iterate over all tweets and print the full text alongside some metadata.
for tweet in tweets:
    # To access any sub-part of a tweet (text or metadata), note that the internal model
    # resembles a dictionary; therefore, each attribute must be accessed as such.
    print("Tweet:", tweet.full_text)
    print("Tweet language:", tweet.lang)
    print("Number of hashtags:", len(tweet.hashtags))
    print("Number of retweets:", tweet.retweet_count)
    print("Location:", tweet.location)
    if tweet.retweeted_status is not None:
        print("Is retweet: Yes")
        #print(tweet.retweeted_status)
        print("Original tweet:", tweet.retweeted_status.full_text)
    else:
        print("Is retweet: No")
        # We add non-retweet tweets (i.e. original tweets) to our List of interest.
        original_tweets.append(tweet)
    print("-----")

print("Number of original tweets out of", len(tweets),"in total:", len(original_tweets))
# Since the List original_tweets contains custom objects defined by the python-twitter library,
# we cannot save them as a plain text file.
# Instead we will save them inside a binary "as-is" file using pickle.
with open("./tweets.obj", "wb") as my_file:
    pickle.dump(original_tweets, my_file)

# NIMBY: Hashtags most associated with 東京五輪
#
# We initialize an empty List to store all hashtags.
all_hashtags = []
for tweet in tweets:
  # Hashtags associated with a tweet are store in a List.
  # Thus, we can simply loop over each element of that List as well.
  for hashtag in tweet.hashtags:
    # As before, the internal model (now for hashtags) necessitates accessing attributes individually.
    all_hashtags.append(hashtag.text)

print("Total number of hashtags:", len(all_hashtags))
fdist = FreqDist(all_hashtags)
print("Total number of distinct hashtags:", len(fdist.keys()))

print("Most common hashtags and their frequencies:")
print(fdist.most_common(50))