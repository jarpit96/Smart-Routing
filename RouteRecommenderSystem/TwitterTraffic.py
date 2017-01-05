# to check the program uncomment the lines from 221 to 235
# req good net to fetch tweets from twitter

from routing.models import State, District, Locality
import tweepy  # for collecting twitter tweets
import re  # for using the regular expression
import nltk  # for NLP tasks
from nltk.tokenize import word_tokenize  # for breaking the words into tokens
import datetime
import googlemaps, pprint, haversine

#  consumer key and access tokens
consumer_key2 = 'ZbYP3gJQtZinjAcpujsM1G6PF'
consumer_secret2 = 'lnloG7zIhcRV1K0eo83ZjxExrxgcJMe2so9BZ0jVDMRx5p6z7e'
access_token2 = '807238567013531650-4Qw1XF70wZyUabTVfij91yHQqWhPVVr'
access_secret2 = 'Ytj875ZcMDsn2vetJaAnoM3v13fPgKJvEYuy8k4YcnVIb'

consumer_key = '7PKbKwOnqwMt7r8v3sCMPq3sO'
consumer_secret = 'jzLIJnrO2vzWAdfOm0hUPwjW0DyMienAaWSjTniXgeTX8Sjt6A'
access_token = '805094868611538944-7fk6IstbfY5BREovvGxn8Nj1oIlF1Z2'
access_secret = 'I1NJfNMGDxghjJCeAeMm7V4t0IhNc3nZ0Jna1uD7xKF5u'

def getTweets():
    # This function will collect all the tweets from handle @dtptraffic
    # and store them in a file **Tweet_delhi_traffic.txt**

    # setting up connection
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    # calculating date previous.. ie. 15days before current date
    datePrevious = datetime.datetime.today() - datetime.timedelta(days=15)

    # opening file to write tweets
    TweetFile = open('Tweet_delhi_trafic.txt', 'a')

    for tweet in tweepy.Cursor(api.user_timeline, id='@dtptraffic', lang='en').items(1000000):

        # added a filter for the number of days = 15
        if (tweet.created_at < datePrevious):
            break

        # getting tweets with label of **Traffic Alert**
        matchTrafficAlert = re.match(r'Traffic Alert', tweet.text, re.M | re.I)

        if (matchTrafficAlert):
            # uncomment line below to see tweets
            # print(tweet.text)
            TweetFile.write(tweet.text.encode('utf-8'))
            TweetFile.write('\n')
        else:
            continue

    TweetFile.close()


def cleanTweets():
    # This function will read the tweets from the file **Tweet_delhi_trafic.txt**
    # clean it and store it in a better form in the file **CleanTweets.txt**

    ReadFile = open('Tweet_delhi_trafic.txt', 'r')
    AppendFile = open('CleanTweets.txt', 'a')

    lines = ReadFile.readlines()

    for line in lines:
        matchAlert = re.match('Traffic Alert', line, re.M | re.I)
        matchBlank = re.match('\n', line, re.M | re.I)
        if (matchAlert or matchBlank):
            continue

        # cleaned tweets written to file
        # uncomment line below to print the lines in console
        # print(line)
        AppendFile.write(line)

    AppendFile.close()
    ReadFile.close()


def getPlacesKeywords():
    # Process the cleaned tweets of the file **CleanTweets.txt** to get
    # Places and Keywords
    # it will return a list All_Tweet_Place_Keyword
    # All_Tweet_Place_Keyword[0]=Tweet (String)
    # All_Tweet_Place_Keyword[1]=Places  (list)
    # All_Tweet_Place_Keyword[2]=Keywords  (list)

    ReadFile = open('CleanTweets.txt', 'r')

    # Set of words that are not places
    NotPlaces = {'traffic', 'Traffic', 'DTC', 'Breakdown', 'breakdown', 'Bus', 'bus', 'rally', 'Rally',
                 'Programme', 'programme', 'procession', 'Procession', 'Sewer', 'sewer', 'Torch', 'torch',
                 'PM', 'Please', 'please', 'kindly', 'Kindly', 'Crane', 'crane', 'tr', 'Tr', 'TR', 'Metro work',
                 'metro work', 'Metro Work', 'Work', 'PWD', 'LGV', 'MGV', 'HTV', 'DJB', 'work',
                 'Truck', 'Tanker', 'Water', 'No', 'No.', 'few'}

    # Set of words that are not keywords (not descriptive words)
    NotKeywords = {'underpass', 'Removed', 'removed', 'Underpass', 'red', 'Red', 'been', 'few', 'gate',
                   'metro', 'advised', 'alternate', 'commercial', 'religious', 'following', 'Due', 'due',
                   'Panchkuian', 'pipe'}

    All_Tweet_Place_Keyword = list()  # store the tweets, places extracted from it and keywords related

    lines = ReadFile.readlines()

    previous_keyword = list()
    # will be used inside the loop to store the keyword of previous tweet

    for tweet in lines:

        Tweet_Place_Keyword = list()  # will combine tweet, place and keyword

        CheckLanguage = re.search('[a-zA-Z]{6,}', tweet)  # will check the tweet for language
        if (not CheckLanguage):  # if hindi, then tweet not processed
            continue

        tweet = re.sub("&amp;", " , ", tweet)  # replacing &amp; with ' , '
        tweet = re.sub('delhi', 'Delhi', tweet)  # replacing delhi with Delhi

        word_tokens = word_tokenize(tweet)  # creating tokens of words
        word_tags = nltk.pos_tag(word_tokens)  # assigning tags to tokens

        # creating list for places and Keywords
        Places = list()
        Keywords = list()

        # Basic adjustment, if string has obstruction in it then append obstruction keyword to keywords list
        matchObstruction = re.match('Obstruction in traffic', tweet, re.M | re.I)
        if (matchObstruction):
            Keywords.append("Obstruction")

        # Basic adjustment, if string has removed in it then append removed keyword to keywords list
        matchRemoved = re.search('removed', tweet, re.M | re.I)
        if (matchRemoved):
            Keywords.append("Removed")

        i = 0  # count will be used to iterate word_tags

        while (i < len(word_tags)):

            if (word_tags[i][1] == 'NNP'):  # if token has tag proper noun

                flag = 0  # will be used to check if token should be added to places or not
                # flag =0  ->  place  ;   flag =1  ->not a place
                key = word_tags[i][0]

                if (key in NotPlaces):
                    flag = 1

                # adjustment for accepting ring road as place
                if (key == 'Road' and i > 0 and word_tags[i - 1][0] == 'Ring'):
                    key = 'Ring Road'
                    i = i + 1
                    Places.append(key)
                    continue

                # adjustment for accepting Panchkuian road as place
                if (key == 'Road' and i > 0 and word_tags[i - 1][0] == 'Panchkuian' and word_tags[i - 1][1] == 'JJ'):
                    key = "Panchkuian Road"
                    i = i + 1
                    Places.append(key)

                j = i + 1  # set j to point to next index

                while (j < len(word_tags) and (
                            word_tags[j][1] == 'NNP' or word_tags[j][1] == 'NN' or word_tags[j][1] == 'CD')):
                    if (word_tags[j][0] in NotPlaces):
                        flag = 1
                        break
                    key = key + " " + word_tags[j][0]
                    j = j + 1

                # rules to check if key is a veh num or just **No.**
                exp_v_num = r"([A-Za-z0-9]*)(\d{4})"
                exp_num = r"No.(\d)"
                matchVNumber = re.search(exp_v_num, key, re.I)
                matchNumber = re.search(exp_num, key, re.I)
                if (matchNumber or matchVNumber):
                    flag = 1

                exp_Part = r'(\d)+/(\d)+'  # exp to check if key contains something like 1/2 or 1/3 etc
                key = re.sub(exp_Part, '', key)

                # setting places to delhi specific places..  like IIT to IIT Delhi
                if (key == 'Chirag'):
                    key = 'Chirag Delhi'

                if (key == 'IIT'):
                    key = 'IIT Delhi'

                if (key == 'Airport'):
                    key = 'IGI Airport'

                if (key == 'AIIMS'):
                    key = 'AIIMS Delhi'

                if (flag == 0):  # if key is a place
                    Places.append(key)

                i = j - 1  # decrementing value of index

            elif (word_tags[i][1] == 'JJ' or word_tags[i][1] == 'VBN'):
                if (word_tags[i][0] not in NotKeywords):
                    Keywords.append(word_tags[i][0])

            i = i + 1

        # if keyword empty for this line, set the kewords same as the keywords of the last tweet
        if (len(Keywords) == 0):
            Keywords = previous_keyword

        previous_keyword = Keywords

        if (len(Places) == 0):
            continue

        Tweet_Place_Keyword.append(tweet)
        Tweet_Place_Keyword.append(Places)
        Tweet_Place_Keyword.append(Keywords)

        All_Tweet_Place_Keyword.append(Tweet_Place_Keyword)

    return All_Tweet_Place_Keyword


#find closest locality using haversine
def findNearestLocality(lat, lng):
    min_dist = float("inf")
    min_locality = ''
    states = State.objects.all()
    for state in states:
        districts = District.objects.filter(state = state)
        for district in districts:
            localities = Locality.objects.filter(district = district)
            for locality in localities:
                dist = haversine.haversine(locality.lat, locality.lng, lat, lng)
                if min_dist > dist:
                    min_dist = dist
                    min_locality = locality.name

    return min_locality

def seTrafficWeights(LIST):
    currkey = 0
    key = ['AIzaSyDmT6F29WJ9M-viNlrMzRpRPtdseHTCfoA', 'AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0',
           'AIzaSyDhic6BCNfkgzsPhsKEkZ_BvZKkzKhXEzs']
    gmaps = googlemaps.Client(key=key[currkey])
    request_cnt = 0
    pp = pprint.PrettyPrinter(indent=4)
    traffic_weights = {'heavy': 1, 'congested': 1.5, 'removed': 3, 'obstruction': 1.5, 'few': 5,
                       'closed': 0, 'normal': 4, 'diverted': 0, 'overturned': 0.5, 'open': 3, 'carried': 1}
    today = datetime.date.today()
    places_traffic_weights = {}
    for x in LIST:
        localities = x[1]
        traffic_conditions = x[2]
        min_weight = 6
        for condition in traffic_conditions:
            if condition in traffic_weights:
                if min_weight > traffic_weights[condition]:
                    min_weight = traffic_weights[condition]
        if min_weight != 6:
            for locality in localities:
                loc = str(locality).split('\\n')
                for l in loc:
                    if l in places_traffic_weights:
                        if places_traffic_weights[l] > min_weight:
                            places_traffic_weights[l] = min_weight
                    else:
                        places_traffic_weights[l] = min_weight


    for p in places_traffic_weights:
        #get coordinates for p
        response = gmaps.geocode(p+', Delhi')
        pp.pprint(response)
        if len(response) != 0:
            lat = response[0]['geometry']['location']['lat']
            lng = response[0]['geometry']['location']['lng']
            locality_name = findNearestLocality(lat, lng)
            print 'locality name closest to : ', p, 'is : ', locality_name
            try:
                l = Locality.objects.get(name = locality_name)
            except Locality.DoesNotExist:
                print 'locality object not found'
                continue
            if (today - l.date).days >= 7:
                print 'Greater Than seven Days passed'
                l.traffic_wt = places_traffic_weights[p]
            else:
                print 'Less than 7 Days'
                l.traffic_wt = min(l.traffic_wt, places_traffic_weights[p])
            l.date = today
            l.save()
            print 'Object saved: ',l.name



#   files used
#   Tweet_delhi_traffic.txt
#   CleanTweets.txt


# checking the program
# uncomment the program below to check the program

def updateTraffic():
    getTweets()
    cleanTweets()
    LIST = list()
    LIST = getPlacesKeywords()

    # for x in LIST:
    #     print('\n****************************')
    #     print(x[0])
    #     print('Places : ',x[1])
    #     print('Keywords : ',x[2])
    seTrafficWeights(LIST)

updateTraffic()