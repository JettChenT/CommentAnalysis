from aip import AipNlp

#init
APP_ID = '16649663'
API_KEY = '3f1OS9Wc5qt8fvBhDsQUhFGe'
SECRET_KEY = 'CH75tnGEtcl6iyguEzSf43fLrpXgVzpM'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
def getsent(text):
    res = client.sentimentClassify(text)
    if 'items' in res.keys():
        return res['items'][0]['sentiment']
    return "error"

def average(list):
    return(sum(list)/len(list))

def analysis(clist):
    # core algorithm, the exciting part
    # improve over time
    slist = []
    for s in clist:
        sen = getsent(s)
        if sen != 'error':
            slist.append(int(getsent(s))-1)
    return average(slist)
