
import numpy as np
import json
from nltk.stem.snowball import SnowballStemmer
from appJar import gui
import time
import os

#basePath= "/Users/therohan_21/PycharmProjects/indextry1/Report"
basePath = os.path.abspath("Report")
print(basePath)
#basePath1="/Users/therohan_21/PycharmProjects/indextry1/Report4 "
basePath1 = os.path.abspath("Report4")
print(basePath1)
with open(basePath, 'r') as json_data:
    d = json.load(json_data)
with open(basePath1, 'r') as json_data1:
    d1 = json.load(json_data1)

print('Done loading to memory')

for a in d:
    for b in d[a]:
        d[a][b] = (1 + np.log10(d[a][b])) * (np.log10(37497/len(d[a])))

for a in d1:
    for b in d1[a]:
        d1[a][b] = (1 + np.log10(d1[a][b])) * (np.log10(37497/len(d1[a])))

#print type(d)

print('Done calculating weights of term in document')

app = gui("Search API", "800x400")
app.setFont(18)
app.addLabel("title", "Please enter")
app.setLabelBg("title", "red")

app.addLabelEntry("Search")
app.setFocus("Search")
query = ''
def press(button):
    if button == "Search":
        global query
        query = app.getEntry("Search")
        time.sleep(2)
        app.stop()


app.addButtons(["Search"], press)
app.go()


stemOutput = SnowballStemmer('english')
print('SEARCH QUERY '+query)

print('calculating query term weight')
a = 0
w = []
query = query.split(" ")
for word in query:
    stemmedquery = stemOutput.stem(word)
    w.append(round(np.log10(37497/len(d[stemmedquery])), 3))


sc = []
scores = {}

print('calculating document scores according to query')
for a in range (len(query)):
    stemmedquery = stemOutput.stem(query[a])
    sc.append(d[stemmedquery])

    if stemmedquery in d1:
        for b in sc[a]:
            if b in d1[stemmedquery]:
                sc[a][b] = (w[a]*d[stemmedquery][b])+(w[a]*d1[stemmedquery][b])*10
    else:
        for b in sc[a]:
            sc[a][b] = w[a]*d[stemmedquery][b]


print('updating the scores based on relevance')
for line in sc:
    for i in line:
        if i in scores:
            #print('in scores')
            scores[i]=scores[i]+line[i]
        else:
            scores[i]=line[i]

u = sorted(scores.items(), key = lambda kv: (kv[1],kv[0]), reverse = True)

print('Retrieving information')

#basePath= "/Users/therohan_21/Python Projects/project3/WEBPAGES_RAW/bookkeeping.json"
basePath = os.path.abspath("WEBPAGES_RAW/bookkeeping.json")
print(basePath)
with open(basePath) as json_data:
    e = json.load(json_data)

def displayres():
    app = gui("Search API", "800x400")
    app.setFont(18)

    for i in range(15):
        l = ''
        t = (str)(i)
        try:
            docid = u[i][0]
            s = e[docid]
            s = (str)(s)
            l = 'http://'+s
            print (type(l))
            app.addWebLink(l,l)
            print (s)
        except:
            app.addLabel(t, "Index Exhausted")
            print('Index Exhausted')
            break
    try:
        app.go()
        app.stop()
    except:
        print('App stopped')


displayres()
