import sqlite3
import json
import re
import tweepy
from tweepy import OAuthHandler
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# create Tweepy connection
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# create sqlite connection
conn = sqlite3.connect('tweets.db')
cur = conn.cursor()


#######################
# CREATE Table Tweets #
#######################

drop_Tweets = "DROP TABLE IF EXISTS Tweets"

create_Tweets = "CREATE TABLE Tweets( \
	tweet_id VARCHAR2(200) PRIMARY KEY,\
	author_id VARCHAR2(200),\
	time_stamp DATE,\
	text VARCHAR2(200)\
)"
# cur.execute(drop_Tweets)
# cur.execute(create_Tweets)


###########################
# INSERT data INTO Tweets #
###########################

# f = open('tweets.json')
# list_of_tuple_to_insert = []
# month_abbr_table = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', \
# 					'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', \
# 				    'Oct':'10', 'Nov':'11', 'Dec':'12'}


# for line in f:	
# 	tweet_id = json.loads(line)['id']
# 	author_id = json.loads(line)['user']['id']
# 	time_stamp = json.loads(line)['created_at']
# 	text = json.loads(line)['text']

# 	# cleanup time_stamp format
# 	# Wed Mar 15 17:21:12 +0000 2017
# 	regaga = r'\w{3} (\w{3}) (\d{2}) (\d{2}:\d{2}:\d{2}) \+0000 (\d{4})'
# 	result = re.match(regaga, time_stamp)
# 	# 2016-09-01 00:00:00
# 	time_stamp = "{year}-{month}-{date} {time}" \
# 				 .format(year=result.group(4), month=month_abbr_table[result.group(1)], date=result.group(2), time=result.group(3))

# 	list_of_tuple_to_insert.append((tweet_id, author_id, time_stamp, text))

# tweets_insertion = "INSERT INTO Tweets VALUES(?,?,?,?)"
# cur.executemany(tweets_insertion, list_of_tuple_to_insert)
# print('Table Tweets has been created and the original Tweets (371) have been inserted')

# f.close()


#
# Create a dictionary to rank the Author based on their mentioned times in UMSI's Tweets
#

# pull_text_from_Tweets_table = "SELECT text FROM Tweets"
# texts = cur.execute(pull_text_from_Tweets_table)

# author_dict = {}
# for text in texts:
# 	text = str(text)
# 	text = text[2:-3]

# 	# use regex to extract the username
# 	word_list = text.split()
# 	for word in word_list:	
# 		result = re.match(r'@(\w+).*', word)
# 		if result:
# 			# switch to all lowercase to remove possible duplicates, causing by having 
# 			# uppercase-lowercase combination
# 			username = result.group(1).lower()
# 			if username not in author_dict:
# 				author_dict[username] = 1
# 			else:
# 				author_dict[username] += 1


# # clean up keys that contain umsi
# author_dict.pop('umsi', None)

# sorted_author_dict = [(k, author_dict[k]) for k in sorted(author_dict, key=author_dict.get, reverse=True)]

# # take out more tweets from the most mentioned user's of umsi
# add_tweet_count = 0
# for k, v in sorted_author_dict:
# 	if add_tweet_count >= 371:
# 		break
# 	print (k, v)

# 	# create a new connection and pull tweets from most mentioned authors of umsi 
# 	try:
# 		for status in tweepy.Cursor(api.user_timeline, id='@'+k).items(20):			
# 			time_stamp = status._json['created_at']
			
# 			# Wed Mar 15 17:21:12 +0000 2017
# 			# clean up the time format
# 			regaga = r'\w{3} (\w{3}) (\d{2}) (\d{2}:\d{2}:\d{2}) \+0000 (\d{4})'
# 			result = re.match(regaga, time_stamp)
			
# 			# 2016-09-01 00:00:00
# 			time_stamp = "{year}-{month}-{date} {time}" \
# 					 .format(year=result.group(4), month=month_abbr_table[result.group(1)],\
# 					         date=result.group(2), time=result.group(3))

			
# 			list_of_tuple_to_insert = []
# 			if time_stamp > '2016-09-01 00:00:00':
# 				add_tweet_count += 1
				
# 				tweet_id = status._json['id']
# 				author_id = status._json['user']['id']
# 				text = status._json['text']

# 				list_of_tuple_to_insert.append((tweet_id, author_id, time_stamp, text))
# 				append_tweets = "INSERT INTO Tweets VALUES(?,?,?,?)"
# 				cur.executemany(append_tweets, list_of_tuple_to_insert)
# 			else:
# 				pass
# 	except Exception as e:
# 		print (e)
# 		pass

# print ('Tweets table have been completed!!')



########################
# CREATE TABLE Authors #
########################

drop_Authors = "DROP TABLE IF EXISTS Authors"

create_Authors = "CREATE TABLE Authors( \
	author_id VARCHAR2(200) PRIMARY KEY, \
	username VARCHAR2(100)\
)"

cur.execute(drop_Authors)
cur.execute(create_Authors)

#####
# select TEXT from the completed Tweets table and populate Authors Table
#####
pull_text_from_Tweets_table = "SELECT text FROM Tweets"
texts = cur.execute(pull_text_from_Tweets_table)


new_author_dict = {}
for text in texts:
	text = str(text)
	text = text[2:-3]

	# use regex to extract the username
	word_list = text.split()
	for word in word_list:	
		result = re.match(r'@(\w+).*', word)
		if result:
			# switch to all lowercase to remove possible duplicates, causing by having 
			# uppercase-lowercase combination
			username = result.group(1).lower()
			if username not in new_author_dict:
				new_author_dict[username] = 1
			else:
				new_author_dict[username] += 1

# # clean up keys that contain umsi
# new_author_dict.pop('umsi', None)

sorted_new_author_dict = [(k, new_author_dict[k]) for k in sorted(new_author_dict, key=new_author_dict.get, reverse=True)]


list_of_tuple_to_insert = []
for k, v in sorted_new_author_dict:
	try:
		user = api.get_user(k)
		screen_name = user._json['screen_name']
		author_id = user._json['id']
		list_of_tuple_to_insert.append((author_id, screen_name))
	except Exception as e:
		pass
	
authors_insertion = "INSERT INTO Authors VALUES(?,?)"
cur.executemany(authors_insertion, list_of_tuple_to_insert)
print('Table Authors has been populated')


##
# CREATE Mentions Table
##

drop_Mentions = "DROP TABLE IF EXISTS Mentions"

create_Mentions = "CREATE TABLE Mentions( \
	tweet_id VARCHAR2(200), \
	author_id VARCHAR2(100)\
)"

cur.execute(drop_Mentions)
cur.execute(create_Mentions)

selection = 'SELECT tweet_id, [text] FROM Tweets'
r = cur.execute(selection)
v = r.fetchall()

list_of_tuple_to_insert = []
for row in v:
	text = row[1]
	tweet_id = row[0]
	word_list = text.split()
	for word in word_list:	
		result = re.match(r'@(\w+).*', word)
		if result:
			username = result.group(1).lower()
			try:
				username_to_author_id = 'SELECT author_id FROM Authors WHERE username = "{}" COLLATE NOCASE'.format(username)
				r = cur.execute(username_to_author_id)
				author_id = r.fetchone()[0] 
			except:
				pass
			list_of_tuple_to_insert.append((tweet_id, author_id))

Mentions_insertion = 'INSERT INTO Mentions VALUES(?,?)'
cur.executemany(Mentions_insertion, list_of_tuple_to_insert)



conn.commit()
conn.close()