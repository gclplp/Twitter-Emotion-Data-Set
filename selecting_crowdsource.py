import random
import pandas as pd

emotions = ["Excited", "Angry", "Fear", "Happy", "Sadness", "Trust"]

"select a random sample of 20 for each of the six emotions"
for word in emotions:
    all_tweets = pd.read_csv(word+".csv", encoding="utf-16", sep="\t")
    print(len(all_tweets))
    index = random.sample(range(0, 149), 20)
    print(index)
    final_tweets = all_tweets.iloc[index]
    print(final_tweets)
    final_tweets.to_csv(word+"_crowd.csv", encoding="utf-16", sep="\t", index=False)