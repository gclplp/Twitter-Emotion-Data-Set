--- INSTRUCTIONS ---
Run rest_api.py first to pull tweet (keys not provided)
Then tweet_cleaner_scorer.py, note that both NRC lexcions are required and included.
Lastly selecting_tweets.py should be run to get a final CSV containing 150 for each emotion.
selecting_crowdsourcing.py is simply how I got a sample for MTurk.

--- OTHER INFORMATION ---
dump of mongodb databse included with the pulled tweets using rest_api.py, depending on the time sometimes the angry
collection has a few less tweets than 450 although this was not an issue for me.
The dump has the raw tweets cleaning and emoitional scoring with tweets_cleaner.py and select the best with selecting_tweets.py
Final tweets for my project in csv folder (selected from the database using selecting_tweets.py).
Crowdsourcing include both the samples I sent for crowdsourcing using sleceting_crowdsourcing.py as well as results.
