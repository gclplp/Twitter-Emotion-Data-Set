from pymongo import MongoClient
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pandas as pd
import re
from nltk.corpus import wordnet

client = MongoClient('mongodb://localhost:27017/')
db = client['twitterdb']
tknzr = TweetTokenizer()

"Setting up hashtag lexicon and EmoLex as well as the list of emotions we used"
hashtag_lexicon = pd.read_table("NRC-Hashtag-Emotion.txt", sep="\t")
hashtag_lexicon.iloc[:,0] = hashtag_lexicon.iloc[:,0].str.title()
only_hashtags = hashtag_lexicon[hashtag_lexicon.iloc[:,1].str.startswith("#", na=False)]
lexicon = pd.read_csv("NRC-Emotion-Lexicon.csv")
emotions = ["#angry", "#happy", "#excited", "#trust", "#sadness", "#scared"]

"A simple list of emojis for four emotions"
happy_emoji = [u"\U0001F600",u"\U0001F601",u"\U0001F602",u"\U0001F603",u"\U0001F923",u"\U0001F66A",u"\U0001F60D"]
angry_emoji = [u"\U0001F612", u"\U0001F624", u"\U0001F621", u"\U0001F620", u"\U0001F44A", u"\U0001F595", u"\U0001F92C"]
fear_emoji = [u"\U0001F616", u"\U0001F631", u"\U0001F628", u"\U0001F627", u"\U0001F97A", u"\U0001F61F", u"\U0001F62C"]
sad_emoji = [u"\U0001F615", u"\U0001F641", u"\U0001F630", u"\U0001F62D", u"\U0001F625", u"\U0001F622", u"\U0001F61E"]

"hashtags that will be used to filter out tweets"
bad_hashtags = ["#followforfollow", "#followback", "#likeforlike", "#follow"]

"""class that deals with repeated characters, compares with the wordnet corpus if not present 
one of repeated character is removed until a mtach is found, ignores hashtags and @"""
class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if word.startswith("@"):
            return word
        elif word.startswith("#"):
            return word
        elif wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word
replacer = RepeatReplacer()


def repeater_letter_cleaner(data):
    text = data["full_text"]
    text = re.sub(r'\.(?=[^ \W\d])', '. ', text)  # deals with bad punctuation
    tokenized = tknzr.tokenize(text)
    for i in range(len(tokenized)):
        tokenized[i] = replacer.replace(tokenized[i])  # each token is checked for repeated characters
    text = TreebankWordDetokenizer().detokenize(tokenized)
    text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)  # cleans issues with detokenizer
    return text


"filters out short tweets ones with bad hashtags and ones with too many hashtags"
def filtering(data):
    if len(data["full_text"]) < 20:
        skip = True
    elif any(word in data["full_text"].lower() for word in bad_hashtags):
        skip = True
    elif len(data["entities"]["hashtags"]) > 7:
        skip = True
    else:
        skip = False
    return skip


"emotional scoring function"
def emo_ranker(data):
    text = data["full_text"]
    tokenized = tknzr.tokenize(text.lower())
    word_frame = lexicon[lexicon["English (en)"].isin(tokenized)]
    total = word_frame.iloc[:,3:11].sum(axis = 0, skipna = True)
    total = total.astype(float)  # first the scores from the EmoLex are added
    if any(word in text for word in happy_emoji):  # checking for the presence of emojis and adding score corresponding
        total["Joy"] += 2
    elif any(word in text for word in angry_emoji):
        total["Anger"] += 2
    elif any(word in text for word in fear_emoji):
        total["Fear"] += 2
    elif any(word in text for word in sad_emoji):
        total["Sadness"] += 2
    hashtag_points = only_hashtags[only_hashtags.iloc[:,1].isin(tokenized)]  # hashtags are examined
    for ind, row in hashtag_points.iterrows():
        total[row[0]] += row[2]  # total score added
    return total

for word in emotions:
    for data in db[word].find():  # loops over every object in every collection
        if filtering(data):
            continue
        data["full_text"] = re.sub(r"http\S+", "", data["full_text"])  # remove links
        data["full_text"] = repeater_letter_cleaner(data)
        data["full_text"] = re.sub(" u ", " you ", data["full_text"])  # corrects u abreviation
        data["full_text"] = re.sub(r'(\w) ’ (.\w{2})', r'\1’ \2', data["full_text"])  # punctuation correction
        data["full_text"] = re.sub(r'(\w) ’ (\w) ', r'\1’\2 ', data["full_text"])  # punctuation correction
        total = emo_ranker(data)
        print(data["full_text"])
        print(total)
        data["emotion_score"] = pd.Series.to_dict(total)  # emotion score is added to every tweet JSON
        db[word + "_scored"].insert(data)  # new collection with filtered and scored tweets, one collection per emotion


"people were found to sometimes tweet the same thing twice this loop removes all duplicates"
for word in emotions:
    check = []
    duplicates = []
    for data in db[word +"_scored"].find():
        if data["full_text"] not in check:
            print(data["full_text"])
            check.append(data["full_text"])
        else:
            duplicates.append(data["id"])
    db[word + "_scored"].remove({'id': {'$in': duplicates}})


"invents a new excitement score"
for data in db["#excited_scored"].find():
    data["emotion_score"]["Excited"] = (4*data["emotion_score"]["Anticipation"]) + data["emotion_score"]["Joy"]
    print(data["emotion_score"]["Excited"])
    db["#excited_scored"].save(data)

