Run rest_api.py first to pull tweet (keys not provided)
Then tweet_cleaner_scorer.py
Lastly selecting_tweets.py should be run to get a final CSV.
selecting_crowdsourcing.py is simply how I got a sample for MTurk.
dump of mongodb databse included with the pulled tweets as well as the cleaned and scored collection using tweet_cleaner_scorer
depending on the time sometimes the anfry collection has a few less tweets than 450 although this was not an issue for me.
Final tweets for my project in csv folder (selected from the database using selecting_tweets.py).
Crowdsourcing include both the samples I sent for crowdsourcing using sleceting_crowdsourcing.py as well as results.
