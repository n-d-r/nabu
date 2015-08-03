# -*- coding: utf-8 -*-

import requests
import time
import re
from bs4 import BeautifulSoup
from article import *

class Domain:    
    def __init__(self):
        self.article_list = []        
        
    def __str__(self):
        return self.domain + ' | ' + self.url        
        
    def _requests_wrapper(self, url):
        attempts = 0
        while attempts < 3:
            r = requests.get(url)
            if r.status_code != 200:        # 200 means success
                attempts += 1
                time.sleep(3)
            else:
                return r      
        return None  
        
    def get_article_urls(self):
        r = self._requests_wrapper(self.url)
        if r == None:
            pass
            # this shoud probably delete the object in question
        else:
            soup = BeautifulSoup(r.text)
            self.extract_links(soup)
            
    def article_obj_generator(self):
        for article_url in self.article_list:
            yield self.article_class(article_url, self.url)
        
class AlJazeera(Domain):
    def __init__(self, url):
        Domain.__init__(self)        
        self.domain = 'Al-Jazeera'          
        self.url = url
        self.article_class = AlJazeeraArticle
    
    def extract_links(self, soup):     
       articles = soup.find_all(href=re.compile('^/news/[0-9]+'))
       for article in articles:
           self.article_list.append('http://www.aljazeera.com' + 
                                    article.get('href'))
       self.article_list = list(set(self.article_list))
        
#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield AlJazeeraArticle(article_url, self.url)
    
    
    
class EUObserver(Domain):
    def __init__(self, url):
        Domain.__init__(self)          
        self.domain = 'EU Observer'        
        self.url = url
        self.article_class = EUObserverArticle
                     
    def extract_links(self, soup):
        regexpr = re.compile('^/[a-z]+/[0-9]+')
        articles = soup.find_all('a')
        
        for article in articles:
            href = article.get('href')
            if not regexpr.search(href) == None:
                self.article_list.append('http://euobserver.com' + href)
        
        self.article_list = list(set(self.article_list))

#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield EUObserverArticle(article_url, self.url)




class ArsTechnica(Domain):
    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'Ars Technica'
        self.url = url
        self.article_class = ArsTechnicaArticle
        
    def extract_links(self, soup):
        articles = soup.find_all('article')
        
        for artl in articles:
            self.article_list.append(self.url + artl.a.get('href'))

        self.article_list = list(set(self.article_list))    
    
#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield ArsTechnicaArticle(article_url, self.url)



class SPIEGELIntl(Domain):
    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'SPIEGEL Intl'
        self.url = url
        self.article_class = SPIEGELIntlArticle
        
    def extract_links(self, soup):
        # main articles        
        artls = soup.find_all(attrs={'class': 'article-title'})
        for artl in artls:
            self.article_list.append('http://www.spiegel.de' + artl.a.get('href'))
        
        # 'Recent stories' articles (in sidebar on the right)
        recent_stories = soup.find(attrs={'class': 'asset-box asset-list-box \
        clearfix'}).find_all('a')
        for artl in recent_stories:
            self.article_list.append('http://www.spiegel.de' + artl.get('href'))
            
        self.article_list = list(set(self.article_list))
        
    
#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield SPIEGELIntlArticle(article_url, self.url)
            
            
            
class BBCNews(Domain):
    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'BBC News'
        self.url = url
        self.article_class = BBCNewsArticle
        
    def extract_links(self, soup):
        a = soup.find_all(attrs={'type': 'application/ld+json'})           
        regex = re.compile('http://www.bbc.com/news/[a-z]+-[a-z]*-*[a-z]*-*[a-z0-9]+/')
        self.article_list = list(set(regex.findall(str(a[1]))))
        # note: there are (usually) two matches found by the first line,
        # the second of which should contain the script including all
        # relevant URLs.
                            
    
#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield BBCNewsArticle(article_url, self.url)
            
            
            
class Euronews(Domain):
    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'euronews'
        self.url = url
        self.article_class = EuronewsArticle

    def extract_links(self, soup):
        self.article_list.append('http://www.euronews.com' + \
            soup.find(attrs={'class': 'topStoryTitle'}).a.get('href'))
        artls = soup.find_all(attrs={'class': 'themeArtTitle'})
        for artl in artls:
            self.article_list.append('http://www.euronews.com' + \
                artl.a.get('href'))
        self.article_list = list(set(self.article_list))
            

#    def article_obj_generator(self):
#        for article_url in self.article_list:
#            yield EuronewsArticle(article_url, self.url)            




                 