#!/usr/bin/env python
# -*- coding: utf-8 -*-  

__version__ = '1.0'
__author__ = 'BaCde'

__doc__ = """
Check Drak Link http://www.bacdewu.com

by BaCde # Insight-labs
email:glacier@insight-labs.org
for Python 2.7
"""

import re
import urllib
import urllib2
import logging
import math
import urlparse
from Queue import Queue
from threading import Thread


threadNum = 15
CheckRegsold  = [
'<div\sid=.*?>.*?</div>\s{0,2}<script>',
'<div\s*style=.{0,1}position.*?(?:top|left):\s*-[\d]{3,4}px.*?>.*?</div>',
'<MARQUEE\s.*?scrollAmount=.?[\d]{4,5}.?.*?(?:width|height)=.?[0-5].?.*?>.*?</marquee>',
'<div\s*style=.?text-indent:\s*-[\d]{2,5}px.?>.*?</div>',
'<div\s*style=.*?position:\s*absolute\s*;\s*(?:top|left)\s*:\s*expression\(.*?\).*?>.*?</div>',
'<MARQUEE[^>]*?width=["\']?[0-9]?\s+height=["\']?[0-9]["\']?[^>]*?>([\s\S]*?)</MARQUEE>',
'<marquee\s+height=[0-9]\s+width=[0-9][^>]*?>([\S\s]*?)</marquee>',
'<div\s+style\s*=\s*["\']*\s*overflow\s*:\s*hidden\s*;\s*height\s*:\d\d?px\s*;\s*width\s*:\s*\d\d?.*?>([\S\s]*?)</div>',
]

CheckRegs  = [
'<marquee\s+height=[0-9]\s+width=[0-9][^>]*?>([\S\s]*?)</marquee>',
'<div\s*?id=.?\w{1,20}?.?>([\S\s]*?)</div>\s*?<script>document\.getElementById\(.*?\)\.style\.display=.?none.?[;]?</script>',
#'<div\s*style=.{0,1}position\s*:\s*absolute.*?(?:top|left):\s*-[\d]{3,4}px.*?>.*?</div>',
'<div\s*style=.{0,1}position\s*:\s*absolute.*?(?:top|left|right):\s*-[6-9][\d]{2,3}px\s*;(?:top|left|right):\s*-[6-9][\d]{2,3}px\s*;.*?>.*?</div>',
#'<div\s*?style=.?\s*?position([\S\s]*?)(?:top|left):\s*?-[\d]{3,4}px([\S\s]*?)>([\S\s]*?)</div>',
#'<MARQUEE\s.*?scrollAmount=.?[\d]{4,5}.?.*?(?:width|height)=.?[0-5].?.*?>.*?</marquee>',
'<div\s*style=.?text-indent:\s*-[\d]{3,5}px.?>([\S\s]*?)</div>',
'<div\s*style=[^>]*?position:\s*absolute\s*;\s*(?:top|left)\s*:\s*expression\(.*?\).*?>.*?</div>',
'<MARQUEE[^>]*?width=["\']?[0-9]?\s+height=["\']?[0-9]["\']?[^>]*?>([\s\S]*?)</MARQUEE>',
'<div\s+style\s*=\s*["\']*\s*overflow\s*:\s*hidden\s*;\s*height\s*:\d\d?px\s*;\s*width\s*:\s*\d\d?.*?>([\S\s]*?)</div>',
'<div\s+(?!.*?class.*?)(?!.*?\bid\b.*?).*?style=display:none.*?>([\S\s]*?)</div>'
]


dicpath = "url.txt"
def get(url):
    #result = ""
    user_agent = 'User-Agent: Mozilla/5.0 ' \
            + '(Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.4) ' \
            + 'Gecko/20070515 Firefox/2.0.0.4'
    try:
        #print("http://"+ url)

        request = urllib2.Request(url)
        request.add_header('User-Agent', user_agent)

        logging.debug('Get.get - getting url ' + url)
        #print("http://"+request)
        result = urllib2.urlopen(request,timeout=20)
        #print result.read()
        return result.read()
    except :
        return "fail"

def CheckLink():
    while True:
        pw = q.get()
        result = get(pw)
        #print pw
        #if content!="":
        if result !="fail":
            #content = result.read()
            content =result
            type=sys.getfilesystemencoding()
            content=content.decode('gbk', 'ignore').encode('utf-8')
            #print(content)
            print(pw + "\n")
            for CheckReg in CheckRegs:
                print "Check:" + CheckReg
                try:
                    startTimeStamp=time.time()
                    pattern = re.compile(CheckReg, re.DOTALL) 
                    tokens = pattern.findall(content)
                    endTimeStamp=time.time()
                    runtime = endTimeStamp-startTimeStamp
                    print "reg " + CheckReg + "\truntime:" + str(runtime) + "\t length: " + str(len(content)) + "\n\r"
                    #logger.info(tokens)
                    #print(tokens)
                    if len(tokens)!=0:
                       
                        for token in tokens:
                            rcontent = token
                            #print(rcontent)
                            rcontent = rcontent.strip()
                            fileh.write(pw + ':\n' + CheckReg + '\n' + rcontent + '\n')
                    #print(pw + '\t' + rcontent)
                    
                except Exception,e:
                    print e
    q.task_done()     

if __name__ == '__main__':
    import os
    import sys
    import time

    import signal
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit())
    global result
    #print 'Threads started'
    fileh=open('./result.txt','w')
    q=Queue()
    #创建线程
    for i in range(threadNum):
        t = Thread(target=CheckLink)
        #t.daemon=True
        #t.setDaemon(True)
        t.start()

    with open(dicpath) as f:
        for line in f:
            rcontent = ''
            pw = line.strip()
            q.put(pw)
            
    f.close()
    #fileh.close()