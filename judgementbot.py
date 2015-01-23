import praw
import string
import heapq
import datetime

from collections import deque



USERNAME = "judgement_bot"
PASSWORD = "1KIZC3Ym"
USERAGENT = "USERNAME by /u/pinkbehemoth v1.0"
SUBREDDIT = "announcements+Art+AskReddit+askscience+aww+blog+books+creepy+dataisbeautiful+DIY+Documentaries+EarthPorn+explainlikeimfive+Fitness+food+funny+Futurology+gadgets+gaming+GetMotivated+gifs+history+IAmA+InternetIsBeautiful+Jokes+LifeProTips+listentothis+mildlyinteresting+movies+Music+news+nosleep+nottheonion+oldschoolcool+personalfinance+philosophy+photoshopbattles+pics+science+Showerthoughts+space+sports+television+tifu+todayilearned+TwoXChromosomes+UpliftinfNews+videos+worldnews+writingprompts"
            
r = praw.Reddit('USERAGENT')
r.login('judgement_bot','1KIZC3Ym')

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
    for x in range(0,index):
        bc = pq.pop()
        text += "\n* **{}** with **{}** karma, by **{}** and can be found [here!]({})".format(x, bc.score, bc.author, bc.permalink)
        
    text+= "\n\nKarma values may have changed since the bot got the data, so there may be a slight inaccuracy. \n\nWas the hate deserved or not? You decide!"
    print(text)
    r.submit('dailyworst', 'Worst of 1/11/2015', text)

pq = PriorityQueue()



running = True
lasttime = datetime.datetime
while running:

    time = datetime.datetime
    i = 0
    #tmp = (int)lasttime.day + 1
    if time:
        lasttime = time

        
        all_comments = r.get_comments(SUBREDDIT, limit = None)
        for comment in all_comments:
            i+=1
            if comment.id in cache:
                #cache[i] = comment
                print("comment already in cache")
            
            elif comment.score < 0:
                cache.append(comment.id)
                #print("putting ", comment.id, " in the queue with: ", comment.score, "karma")
                pq.push(comment, comment.score)

        worst_ten(pq)

        print("found ", i, " comments")

    break

        

