import logging
logging.basicConfig(filename='log.log',level=logging.DEBUG)



import sched, time, datetime
s = sched.scheduler(time.time, time.sleep)
import urllib2
import requests
from BeautifulSoup import BeautifulSoup
url=""
api_base='https://api.telegram.org/bot.../sendMessage'
global ls
ls=[]

global os
os=[]

global count
count=0

def refresh():
    global ls
    global os
    global count

    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        mydivs = soup.findAll("div", { "class" : "ten column" })
        l=['Dubai Students: '+mydivs[0].ul('li')[1].text.strip('Next available appointment for Iranian students:'),
        'Yerevan Students: '+mydivs[1].ul('li')[1].text.strip('Next available appointment for Iranian students:'),
        'Ankara Students: '+mydivs[2].ul('li')[1].text.strip('Next available appointment for Iranian students:')]
        if (ls!=l):
            ls=l
            if (count!=0):
                print l;logging.debug(l)

                ls_str= '\n'.join(ls)+'\nFor non-student visa check @us_visa_nonstudents'
                api_url1=api_base+'?text='+ls_str+'&chat_id=@us_visa_channel'
                response1 = requests.get(api_url1)

        o=['Dubai Non-students: '+mydivs[0].ul('li')[2].text.strip('Next available appointment for all other visa categories:'),
        'Yerevan Non-students: '+mydivs[1].ul('li')[2].text.strip('Next available appointment for all other visa categories:'),
        'Ankara Non-students: '+mydivs[2].ul('li')[2].text.strip('Next available appointment for all other visa categories:')]
        if (os!=o):
            os=o
            if (count!=9):
                print o;logging.debug(o)

                os_str= '\n'.join(os)+'\nFor student visa check @us_visa_channel'
                api_url2=api_base+'?text='+os_str+'&chat_id=@us_visa_nonstudents'
                api_url2=api_base+'?text='+os_str+'&chat_id=@visatest'
                response2 = requests.get(api_url2)
    except:
        print 'error'
        logging.debug('error')

    return 

def do_something(sc): 
    global count
    now_time=datetime.datetime.now()
    logging.debug(now_time)
    refresh()
    count=1
    sc.enter(1, 1.5, do_something, (sc,))

s.enter(1, 1.5, do_something, (s,))
s.run()
