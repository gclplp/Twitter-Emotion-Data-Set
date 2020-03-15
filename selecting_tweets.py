from pymongo import MongoClient
import pymongo
import csv

client = MongoClient('mongodb://localhost:27017/')
db = client['twitterdb']


"Simply selecting the top 150 tweets for each emotion by their corresponding emotion and storing in csv"
with open('Happy.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#happy_scored"].find().sort("emotion_score.Joy", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Joy"])

with open('Angry.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#angry_scored"].find().sort("emotion_score.Anger", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Anger"])

with open('Fear.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#scared_scored"].find().sort("emotion_score.Fear", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Fear"])

with open('Trust.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#trust_scored"].find().sort("emotion_score.Trust", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Trust"])

with open('Sadness.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#sadness_scored"].find().sort("emotion_score.Sadness", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Sadness"])

with open('Excited.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["id", "full_text", "created_at"])
    for data in db["#excited_scored"].find().sort("emotion_score.Excited", pymongo.DESCENDING).limit(150):
        writer.writerow([(data["id"]), (data["full_text"]), (data["created_at"])])
        print(data["full_text"])
        print(data["emotion_score"]["Excited"])
