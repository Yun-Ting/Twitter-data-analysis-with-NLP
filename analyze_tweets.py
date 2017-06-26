import tweepy
from tweepy import OAuthHandler
import json
import sqlite3
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import re
import nltk


conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

# Authorization setup to access the Twitter API
# auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)

# json_file = open('tweets.json','w')
# for status in tweepy.Cursor(api.user_timeline, id="@umsi").items(371):
# 	# last id to retrieve : 771353294711222272
#     json_str = json.dumps(status._json)
#     json_file.write(json_str + '\n')

# json_file.close()


# print('***** MOST FREQUENTLY MENTIONED AUTHORS *****')

# q = 'SELECT m.author_id, count(m.author_id), a.username '
# q += 'FROM Mentions m '
# q += 'JOIN Authors a ON m.author_id = a.author_id '
# q += 'GROUP BY m.author_id '
# q += 'ORDER BY count(m.author_id) DESC '

# r = cur.execute(q)
# count = 0
# for row in r.fetchall():
# 	count += 1
# 	if count < 10:
# 		print (row[2],"is mentioned", row[1], "times")
# 	else:
# 		break

# print('*' * 20, '\n\n') # dividing line for readable output

# print('***** TWEETS MENTIONING AADL *****')

# q = 'SELECT t.text, m.author_id '
# q += 'FROM Tweets t JOIN Mentions m '
# q += 'ON t.tweet_id = m.tweet_id '
# q += 'WHERE m.author_id = "13602482"'

# r = cur.execute(q)
# for row in r.fetchall():
# 	print (row[0])

# print('*' * 20, '\n\n')



print('***** MOST COMMON VERBS IN UMSI TWEETS *****')

# Print the 10 most common verbs ('VB' in the default NLTK part of speech tagger) 
# that appear in tweets from the umsi account
q = 'SELECT text FROM Tweets WHERE author_id = "18033550"'
r = cur.execute(q)

umsi_token_dict = {}
for row in r.fetchall():
	tokens = nltk.word_tokenize(row[0]) # split the words in the sentence into a list of words
	tagged_tokens = nltk.pos_tag(tokens) # gives us a tagged list of tuples
	# print(tokens)
	# print(tagged_tokens)
	for a, b in tagged_tokens:
		if b == "VB":
			# print (a, b)
			if a not in umsi_token_dict:
				umsi_token_dict[a] = 1
			else:
				umsi_token_dict[a] += 1

umsi_token_dict.pop('@', None)
sorted_umsi_token_dict = [(k, umsi_token_dict[k]) for k in sorted(umsi_token_dict, key=umsi_token_dict.get, reverse=True)]

count = 0
for k, v in sorted_umsi_token_dict:
	if count < 10:
		print (k, v)
		count += 1
	else:
		break



print('*' * 20, '\n\n')



print('***** MOST COMMON VERBS IN UMSI "NEIGHBOR" TWEETS *****')

# Print the 10 most common verbs ('VB' in the default NLTK part of speech tagger) 
# that appear in tweets from umsi's "neighbors", giving preference to tweets from
# umsi's most "mentioned" accounts

q = 'SELECT text FROM Tweets WHERE author_id != "18033550"'
r = cur.execute(q)

umsi_token_dict = {}
for row in r.fetchall():
	tokens = nltk.word_tokenize(row[0]) # split the words in the sentence into a list of words
	tagged_tokens = nltk.pos_tag(tokens) # gives us a tagged list of tuples
	# print(tokens)
	# print(tagged_tokens)
	for a, b in tagged_tokens:
		if b == "VB":
			# print (a, b)
			if a not in umsi_token_dict:
				umsi_token_dict[a] = 1
			else:
				umsi_token_dict[a] += 1

umsi_token_dict.pop('@', None)
sorted_umsi_token_dict = [(k, umsi_token_dict[k]) for k in sorted(umsi_token_dict, key=umsi_token_dict.get, reverse=True)]

count = 0
for k, v in sorted_umsi_token_dict:
	if count < 10:
		print (k, v)
		count += 1
	else:
		break


print('*' * 20, '\n\n')


conn.close()