import praw
import string
import heapq
import datetime
import time

from collections import deque

DAILY_RUN_TIME = "06:30"

USERNAME = "judgement_bot"
PASSWORD = "1KIZC3Ym"
USERAGENT = "USERNAME by /u/pinkbehemoth v1.0"
SUBREDDIT = "announcements+Art+AskReddit+askscience+aww+blog+books+creepy+dataisbeautiful+DIY+Documentaries+EarthPorn+explainlikeimfive+Fitness+food+funny+Futurology+gadgets+gaming+GetMotivated+gifs+history+IAmA+InternetIsBeautiful+Jokes+LifeProTips+listentothis+mildlyinteresting+movies+Music+news+nosleep+nottheonion+oldschoolcool+personalfinance+philosophy+photoshopbattles+pics+science+Showerthoughts+space+sports+television+tifu+todayilearned+TwoXChromosomes+UpliftinfNews+videos+worldnews+writingprompts"
            


cache = deque(maxlen = None)



class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self): 
        return heapq.heappop(self._queue)[-1]


def worst_ten(pq):

    if pq._index < 10:
        index = pq._index
    else:
        index = 10
        
    #here i construct the message to be posted
    text = "The results are in! The top ten most downvoted posts of the past 24 hours are as follows: \n"     
    for x in range(1,index+1):
        bc = pq.pop()
        text += "\n* **{}** with **{}** karma, by **{}** and can be found [here!]({})".format(x, bc.score, bc.author, bc.permalink)
        
    text+= "\n\nKarma values may have changed since the bot got the data, so there may be a slight inaccuracy. \n\nWas the hate deserved or not? You decide!"
    print(text)
    r.submit('dailyworst', 'Worst of '+ time.strftime("%m/%d/%y"), text)

pq = PriorityQueue()

def get_todays(subreddits):
    for post in subreddits.get_new(limit = None):
        if post.created_utc < YESTERDAY:
            yield post
        else:
            break

running = True
lasttime = datetime.datetime
while running:

    i = 0
    c_time = time.strftime("%H:%M")
    print(c_time + "==" + DAILY_RUN_TIME + ": " + str(c_time == DAILY_RUN_TIME))

    if c_time == DAILY_RUN_TIME:
        TODAY = time.time()
        YESTERDAY = TODAY -(24*60*60)

        print("logging in")
		
        r = praw.Reddit('USERAGENT')
        r.login('judgement_bot','1KIZC3Ym')
        
        print("scrounging reddit...")
        all_comments = r.get_comments(SUBREDDIT, time='day', limit = None)
        for comment in all_comments:
            #print(comment.created)
            if comment.id in cache or comment.created_utc < YESTERDAY:
                #cache[i] = comment
                #print("comment ignored")
                continue
            elif comment.score < 0:
                i+=1
                cache.append(comment.id)
                print("putting ", comment.id, " in the queue with: ", comment.score, "karma")
                pq.push(comment, comment.score)

        worst_ten(pq)

        print("found ", i, " comments")
		
        
        r.clear_authentication()

    

        

