from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import scrapy
import os
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
                link = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={pn}&type=1&oid={oid}&sort=1'.format(oid=avnum,pn=str(pn))
                data = requests.get(link).json()
                if data['code'] == 0:
                    if data['data']['replies']:
                        for item in data['data']['replies']:
                            comments.append(stp_gbk(item['content']['message']))
                    else:
                        break
                else:
                    break
                if pn == 4:
                    break
                pn += 1
            if comments == []:
                return comments,3
            return comments,0
        elif 'youku' in link:
            pass
        return [],1 #1 stands for unsupported site
    else:
        return [],2 #2 stands for not a link

# example:
# print(getcomment('https://www.bilibili.com/video/av40087966?from=search&seid=3180529922178376876'))