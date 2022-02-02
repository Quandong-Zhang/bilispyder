import requests
import random
import re
import time
import json
import sqlite3

SESSDATA=['your ssdata']

# 随机SESSDATA，多个SESSDATA时很有用
def random_SESSDATA(SESSDATA):
    result = random.choice(SESSDATA)
    return result

# 随机UA标
def random_user_agent():

    # 复制的，不知道还有用没
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; "
        "SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; "
        "SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; "
        "Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; "
        "Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; "
        ".NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; "
        "Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; "
        ".NET CLR 3.5.30729; .NET CLR 3.0.30729; "
        ".NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; "
        "Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; "
        "InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) "
        "AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) "
        "Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ "
        "(KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; "
        "rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) "
        "Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) "
        "Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) "
        "Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 "
        "(KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
        "AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) "
        "Presto/2.9.168 Version/11.52",
    ]
    result = random.choice(USER_AGENTS)
    return result

req_headers = {
        'User-Agent': random_user_agent(),
        'Cookie': 'SESSDATA='+random_SESSDATA(SESSDATA)+';',
        'Referer': 'https://www.bilibili.com/',
        'Origin': 'https://www.bilibili.com'
                }


def get(url,headers=req_headers):
    #print("1")
    time.sleep(6)#延时，防被封ip，自行调整
    while True:
        #proxy=reapxy()
        try:
            req=requests.get(url,headers=headers,)#proxies={"https": "https://{}".format(proxy)})
            if jsonl( req.text)['code']==0 or jsonl( req.text)['code']==-404:
                #print("2")
                break
            else:
                #print("3")
                time.sleep(300)
        except:
            pass
    return req


def chinese(html):
    return re.findall(r'[\u4e00-\u9fa5]+', html,)

def jsonl(j_string):
    return json.loads(j_string)

def get_api(aid):
    e = get("https://api.bilibili.com/x/web-interface/view?aid="+str(aid))
    return e

def main():
    for i in range(2,593280000):
        r = get_api(i)
        print(r.text)
        if r.status_code==404 or jsonl(r.text)["code"]==-404:
            print("av",i,"挂了")
            continue
        json_datas=jsonl(r.text)['data']
        #sqlHERE
        conn = sqlite3.connect("bili.db")
        cursor = conn.cursor()
        #sqlEND
        try:
            json_datas['mission_id']
        except:
            json_datas['mission_id'] = -1
        print(json_datas['mission_id'])
        cursor.execute('insert into video (bvid,aid,videos,tid,tname,copyright,pic,title,pubdate,ctime,desc,duration,mission_id,mid,name,h,w) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(json_datas['bvid'],json_datas['aid'],json_datas['videos'],json_datas['tid'],json_datas['tname'],json_datas['copyright'],json_datas['pic'],json_datas['title'],json_datas['pubdate'],json_datas['ctime'],json_datas['desc'],json_datas['duration'],json_datas['mission_id'],json_datas['owner']['mid'],json_datas['owner']['name'],json_datas['dimension']['height'],json_datas['dimension']['width']))
        cursor.close()
        conn.commit()
        conn.close()
        print("av",i,"爬取完毕")



if __name__=="__main__":
    main()