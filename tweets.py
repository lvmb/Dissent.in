import sqlite3

def count_tweets(cursor, cmd):
	lines = 0
	lst = list()
	cursor.execute(cmd)
	for tweet in cursor.fetchall():
		lst.append(tweet)
		lines += 1
	return lines	

def build_tweet(cursor, tweet):
	t_id = 'Tweet ID: %s' % tweet[0]
	t_date = 'Tweet Date: %s' % tweet[1]
	t_text = 'Tweet Text: %s' % tweet[2]
	t_geo = 'Tweet Location: %s' % tweet[3]
	t_keyword = 'Tweet Keyword: %s' % tweet[4]
	t = t_id + '\n' + t_date + '\n' + t_text + '\n' + t_keyword + '\n'
	return t	

def show_tweets(cursor):
	cmd = "select * from tweets"
	cursor.execute(cmd)
	for tweet in cursor.fetchall():
		print build_tweet(cursor, tweet)	    
	print '-----All Tweets: %s' % count_tweets(cursor, cmd)

def show_tweet_count(cursor):
	cmd = "select * from tweets"
	print '-----All Tweets: %s' % count_tweets(cursor, cmd)


def filter_by_keyword(cursor):
 	keyword = raw_input('Keyword > ')
 	t = (keyword, )
 	cursor.execute("select * from tweets where keyword = ?", t)
 	for tweet in cursor.fetchall():
 		print build_tweet(cursor, tweet)

def main(cursor):

	show_tweets(cursor)
	filter_by_keyword(cursor)
	
if __name__ == '__main__':
    conn = sqlite3.connect('tweets.db')
    conn.text_factory = str
    cur = conn.cursor()
    main(cur)
