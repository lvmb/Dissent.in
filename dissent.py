import json, sqlite3, string, sys, time, os.path
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

def createDB(name):
	""" Connect to database. If it doesn't exist, then create it. """	
	ext = '.db'
	db = name+ext
	
	if os.path.isfile(db):
		print 'found %s, resuming scraping' % db
	else:
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('create table tweets (id text, date text, tweet text, geo text, keyword text)')
		print 'created database'

def getDate(self, data):
	""" Parse the date of a raw tweet output as YYYY-MM-DD HH:MM:SS """	
	d = string.split( data['created_at'], ' ')
	ds = ' '.join([d[1], d[2], d[3], d[5] ])
	dt = time.strptime(ds, '%b %d %H:%M:%S %Y')
	d = time.strftime('%Y-%m-%d %H:%M:00', dt)			
	return d
	
def getText(self, data):
	""" Parse the actual text of a raw tweet and do stuff do it """	
	t = str(data['text'].encode('utf-8'))
	return t

def terms():
	""" The keywords to scan the tweet stream for """	
	keywords = ['dissent','protest','sosvenezuela']		
	return keywords

	
def getKeywords(self, data):
	""" Parse returned tweet for keywords """	
	tweet = getText(self, data)
	tweet = tweet.lower()
	keywords = terms()
	
	for i in range(len(keywords)):
 		if keywords[i] in tweet:
 			return keywords[i]
	

def buildTweet(self, data):	
	""" Build the tweet """	
	tweet = {}
	tweet['id'] = str(data['id'])
	tweet['date'] = getDate(self, data)
	tweet['text'] = getText(self, data)
	tweet['geo'] = str(data['geo'])
	tweet['keyword'] = getKeywords(self, data)
	return tweet


def addTweet(self, data):
	""" Add tweet to database """	
	tweet = buildTweet(self, data)
	t = (tweet['id'], tweet['date'], tweet['text'], tweet['geo'], tweet['keyword'])	
	conn = sqlite3.connect("tweets.db")
	conn.text_factory = str
	c = conn.cursor()
	c.execute('insert into tweets values (?,?,?,?,?)', t)
	conn.commit()
	c.close()
	

	print 'added tweet id--> %s' % tweet['id']
	print 'tweet keyword---> %s' % tweet['keyword'] 
	print '\n'

class MyStreamer(TwythonStreamer):	

	createDB(name="tweets")
	
	def on_success(self, data):	
		if 'text' in data:
			addTweet(self, data)

	def on_error(self, status_code, data):
		print status_code
		self.disconnect()



keywords = terms()
stream = MyStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track=keywords)     
