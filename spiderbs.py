# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:09:53 2017

@author: Tana
"""
import requests
from bs4 import BeautifulSoup
from  requests.exceptions import RequestException
import codecs
import json
import multiprocessing
score=[]
index=[]
actor=[]
title=[]
def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'lxml')
            #print soup.prettify()
            return soup
        else:
            return None
    except RequestException:
        return None
def parse_one_page(soup):

    score_integer=soup.find_all('i','integer')
    score_fraction=soup.find_all('i','fraction')
    
    index=soup.find_all('i','board-index')
    actor=soup.find_all('p','star')
    time=soup.find_all('p','releasetime')
    #also can use select method
    #title=soup.select('a[class="image-link"]')[0].get('title')  
    title=soup.find_all('a','image-link') 
    image=soup.find_all('img','board-img')
    for i in range(len(title)):
        yield{ 
             "index":index[i].get_text(),
             "title":title[i].get('title'),
             "actor":actor[i].get_text().strip()[3:],
             "time":time[i].get_text().strip()[5:],
             "score":score_integer[i].get_text()+score_fraction[i].get_text(),
             "image":image[i].get('data-src')
              
             }
    
def write_one_page(content):
    f=codecs.open('resultbs.txt','a','utf-8')
    f.write(json.dumps(content,ensure_ascii=False)+'\n')
    f.close
    #print soup.data-src
def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    soup=get_one_page(url)
   
    #comment=parse_one_page(soup)
    for item in parse_one_page(soup):
        write_one_page(item)
if __name__=='__main__':
    pool=multiprocessing.Pool()
    pool.map(main,[i*10 for i in range(10)])
        
        

