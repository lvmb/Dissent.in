import sqlite3

def main(cursor):
    cursor.execute("select * from tweets")
    for tweet in cursor.fetchall():
        tid = tweet[0]
        tdate = tweet[1]
        text = tweet[2]
        geo = tweet[3]
        t = str(tdate + text + geo)
        
        print '-----tweet: %s ' % text
        print '------date: %s'  % tdate
        print '-------geo: %s'  % geo
        print '----length: %s' % len(text)
        print '\n'

if __name__ == '__main__':
    conn = sqlite3.connect('tweets.db')
    conn.text_factory = str
    cur = conn.cursor()
    main(cur)
