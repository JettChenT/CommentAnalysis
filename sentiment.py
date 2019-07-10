from aip import AipNlp
import math
#init
APP_ID = '16649663'
API_KEY = '3f1OS9Wc5qt8fvBhDsQUhFGe'
SECRET_KEY = 'CH75tnGEtcl6iyguEzSf43fLrpXgVzpM'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
def getsent(text):
    res = client.sentimentClassify(text)
    if 'items' in res.keys():
        return float(res['items'][0]['positive_prob'])-float(res['items'][0]['negative_prob'])
    return "error"

def average(list):
    return(sum(list)/len(list))

def analysis(clist):
    # core algorithm, the exciting part
    # improve over time
    print(clist)
    slist = []
    for s in clist:
        sen = getsent(s)
        if sen != 'error':
            slist.append(sen)
    for i in range(len(slist)):
        slist[i] = round(slist[i],1)
    print(slist)
    retlist = []
    for n in range(-10,11):
        retlist.append(slist.count(n/10))
    return retlist