import tweepy
import re


ckey='ZbYP3gJQtZinjAcpujsM1G6PF'
csecret='lnloG7zIhcRV1K0eo83ZjxExrxgcJMe2so9BZ0jVDMRx5p6z7e'
atoken='807238567013531650-4Qw1XF70wZyUabTVfij91yHQqWhPVVr'
asecret='Ytj875ZcMDsn2vetJaAnoM3v13fPgKJvEYuy8k4YcnVIb'

auth2=tweepy.OAuthHandler(ckey,csecret)
auth2.set_access_token(atoken,asecret)

api=tweepy.API(auth2)
i=1
j=0
for tweet in tweepy.Cursor(api.user_timeline,id='@uptrafficpolice',q='traffic smooth',lang='en').items(100000):
    matchObj = re.match(r'Traffic Alert', tweet.text, re.M | re.I)
    print(i, " : ", tweet.text)
    i = i+1