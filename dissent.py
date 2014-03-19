import json, sqlite3, string, sys, time
from twython import TwythonStreamer, Twython

## Need to actually figure out how to do this securely and properly.
APP_KEY = ''
APP_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, APP_SECRET)

OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
## 

def createDB():
	conn = sqlite3.connect("tweets.db")
	c = conn.cursor()
	c.execute('create table tweets (id text, date text, tweet text, geo text, keyword text)')
	print 'created database'

def getDate(self, data):
	d = string.split( data['created_at'], ' ')
	ds = ' '.join([d[1], d[2], d[3], d[5] ])
	dt = time.strptime(ds, '%b %d %H:%M:%S %Y')
	d = time.strftime('%Y-%m-%d %H:%M:00', dt)			
	return d
	
def getText(self, data):
	t = str(data['text'].encode('utf-8'))
	t = t.lower()
	return t

def buildTweet(self, data):	
	tweet = {}
	tweet['id'] = str(data['id'])
	tweet['date'] = getDate(self, data)
	tweet['text'] = getText(self, data)
	tweet['geo'] = str(data['geo'])
	tweet['keyword'] = getKeywords(self, data)
	return tweet

def addTweet(self, data):
	tweet = buildTweet(self, data)
	t = (tweet['id'], tweet['date'], tweet['text'], tweet['geo'], tweet['keyword'])	
	conn = sqlite3.connect("tweets.db")
	conn.text_factory = str
	c = conn.cursor()
	c.execute('insert into tweets values (?,?,?,?,?)', t)
	conn.commit()
	c.close()
	

	print 'added tweet id %s' % tweet['id']
	print '----------date %s' % tweet['date']
	print '---------tweet %s' % tweet['text']
	print '-----------geo %s' % tweet['geo']
	print '-------keyword %s' % tweet['keyword'] 


def terms():
	keywords = ['dissentin','dissent','martial','curfew','protest','arrested']		
	return keywords

	
def getKeywords(self, data):
	tweet = getText(self, data)
	keywords = terms()
	matched = {}
	unmatched = {}

	for i in range(len(keywords)):
 		if keywords[i] in tweet:
 			matched[i] = keywords[i]
 			return matched[i]
 		else:
 			unmatched[i] = keywords[i]

class MyStreamer(TwythonStreamer):	

# 	createDB()
	
	def on_success(self, data):	
		if 'text' in data:
			addTweet(self, data)

	def on_error(self, status_code, data):
		print status_code
		self.disconnect()



keywords = terms()
stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track=keywords)        
