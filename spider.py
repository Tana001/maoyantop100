# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:23:46 2017

@author: Tana
"""
import requests
import codecs
import json
from requests.exceptions import RequestException 
import re
import  multiprocessing 



def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            response=response.text
            return response
        else:
            return None
    except RequestException:
        return None
        
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name">'
                      +'<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">'
                      +'(.*?)</i>.*?fraction">(\d+)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            "index":item[0],
             "title":item[2],
             "actor":item[3].strip()[3:],
             "time":item[4].strip()[5:],
             "score":item[5]+item[6] ,
             "image":item[1]
            
         }
    
  
def write_to_file(content): 
    with codecs.open('result.txt','a','utf-8') as f:
        
        
   # f=codecs.open('result.txt','a','utf-8') 
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
  

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
    
   # print html
    
if __name__=='__main__':
    pool=multiprocessing.Pool()
    pool.map(main,[i*10 for i in range(10)])
       
