from bs4 import BeautifulSoup
import urllib.request
import requests
import re
# import scrapy
import os
from json import loads
PAGEMAX= 2
def stp_gbk(comment):
    encoded = str(comment).encode('gbk',errors='replace')
    decoded = encoded.decode('gbk')
    return decoded
def getcomment(link):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex,link):    
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        if 'bilibili' in link:
            comments = []
            regex = re.compile(r'av\d*')
            re.findall(regex,link)[0]
            avnum = re.findall(regex,link)[0]
            lav = list(avnum)
            lav.remove('a')
            lav.remove('v')
            avnum = ''.join(lav)
            pn = 1
            while True:
                url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={pn}&type=1&oid={oid}&sort=1'.format(oid=avnum,pn=str(pn))
                data = requests.get(url).json()
                if data['code'] == 0:
                    if data['data']['replies']:
                        for item in data['data']['replies']:
                            comments.append(stp_gbk(item['content']['message']))
                    else:
                        break
                else:
                    break
                if pn == PAGEMAX:
                    break
                pn += 1
            if comments == []:
                return comments,3
            return comments,0
        elif 'youku' in link:
            commentlist = []
            p = urllib.request.urlopen(link)
            soup = BeautifulSoup(p,'html.parser')
            page = str(soup)
            regex = re.compile(r"videoId: '\d*'")
            videoId = re.findall(regex,page)[0][10:-1]
            temp = "https://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList&app=100-DDwODVkv&objectId={objid}&objectType=1&listType=0&currentPage={pn}&pageSize=30&sign=552d9a88b24f4bd83a57b09536bdd4d5&time=1562134877"
            pn=1
            while True:
                url = temp.format(objid=videoId,pn=str(pn))
                r = requests.get(url)
                text = r.text
                lt = list(text)
                start = lt.index('(')
                end = lt.index(')')
                res = ''.join(lt[start+1:end])
                data = loads(res)
                if data['code']==0:
                    if data['data']['comment']:
                        for item in data['data']['comment']:
                            commentlist.append(item['content'])
                    else:
                        break
                else:
                    break
                if pn==PAGEMAX:
                    break
                pn+=1
                # print(commentlist)
            return commentlist,0
        elif 'v.qq.com' in link:
            p = urllib.request.urlopen(link)
            soup = BeautifulSoup(p)
            page = str(soup)
            regex = re.compile(r"\"comment_id\":\"\d*\"")
            commentId=re.findall(regex,page)[0]
            commentId = commentId[14:-1]
            temp= "https://video.coral.qq.com/varticle/{commentId}/comment/v2?callback=_varticle{commentId}commentv2&orinum=10&oriorder=o&pageflag={pn}&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1562297494182"
            pn = 1
            while True:
                url = temp.format(commentId=commentId,pn=pn)
                r = requests.get(url)
                data = loads(r.text[29:-1])
                commentList = []
                for item in data['data']['oriCommList']:
                    commentList.append(item['content'])
                if not data['data']['hasnext']:
                    break
                if pn == PAGEMAX:
                    break
                pn+=1
            print(commentList)
            return commentList,0
        return [],1 #1 stands for unsupported site
    else:
        return [],2 #2 stands for not a link

# example:
# print(getcomment('https://www.bilibili.com/video/av40087966?from=search&seid=3180529922178376876'))
