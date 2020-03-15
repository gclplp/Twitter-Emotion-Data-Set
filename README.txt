--- INSTRUCTIONS ---
Run rest_api.py first to pull tweet (keys not provided)
Then tweet_cleaner_scorer.py, note that both NRC lexcions are required and included.
Lastly selecting_tweets.py should be run to get a final CSV.
selecting_crowdsourcing.py is simply how I got a sample for MTurk.

--- OTHER INFORMATION ---
dump of mongodb databse included with the pulled tweets as well as the cleaned and scored collection using tweet_cleaner_scorer
depending on the time sometimes the anfry collection has a few less tweets than 450 although this was not an issue for me.
To see how the the tweets are pulled its best to run rest_api.py and then tweet_cleaner_scorer.py as this gives perspective
on what each of them does.
Final tweets for my project in csv folder (selected from the database using selecting_tweets.py).
Crowdsourcing include both the samples I sent for crowdsourcing using sleceting_crowdsourcing.py as well as results.
