# -*- coding: utf-8 -*-

"""
This file contains classes to handle the individual news websites ('domains'). 
It also includes domain-related functions and constants.
"""

#===============================================================================
# Imports
#===============================================================================

import requests
import time
import re
import sqlite3
from bs4 import BeautifulSoup

from articles import (Article, EUObserverArticle, AlJazeeraArticle,
                      ArsTechnicaArticle, SPIEGELIntlArticle, BBCNewsArticle, 
                      EuronewsArticle)

#===============================================================================
# Class definitions
#===============================================================================

class Domain:
    """
    Main class for a domain. Domain, here, refers to a particular news 
    platform, such as BBC news. It should not be used directly but inherited
    from by domain-specific subclasses.
    """

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
        if not r:
            pass
        else:
            soup = BeautifulSoup(r.text)
            self.extract_links(soup)
            
    def article_obj_generator(self):
        for article_url in self.article_list:
            yield self.article_class(article_url, self.url)
        


class AlJazeera(Domain):
    """
    Class to handle http://www.AlJazeera.com domain, includes site-specific
    HTML parsing.
    """

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
    
    
    
class EUObserver(Domain):
    """
    Class to handle http://euobserver.com domain, includes site-specific
    HTML parsing.
    """

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



class ArsTechnica(Domain):
    """
    Class to handle http://arstechnica.com domain, includes site-specific
    HTML parsing.
    """

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



class SPIEGELIntl(Domain):
    """
    Class to handle http://www.spiegel.de domain, includes site-specific
    HTML parsing.
    """

    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'SPIEGEL Intl'
        self.url = url
        self.article_class = SPIEGELIntlArticle
        
    def extract_links(self, soup):
        # main articles        
        artls = soup.find_all(attrs={'class': 'article-title'})
        for artl in artls:
            self.article_list.append('http://www.spiegel.de' + 
                                     artl.a.get('href'))
        
        # 'Recent stories' articles (in sidebar on the right)
        recent_stories = soup.find(attrs={'class': 'asset-box asset-list-box \
        clearfix'}).find_all('a')
        for artl in recent_stories:
            self.article_list.append('http://www.spiegel.de' + artl.get('href'))
        self.article_list = list(set(self.article_list))
            
            
            
class BBCNews(Domain):
    """
    Class to handle http://www.bbc.com/news domain, includes site-specific
    HTML parsing.
    """

    def __init__(self, url):
        Domain.__init__(self)
        self.domain = 'BBC News'
        self.url = url
        self.article_class = BBCNewsArticle
        
    def extract_links(self, soup):
        a = soup.find_all(attrs={'type': 'application/ld+json'})           
        regex = re.compile(
            'http://www.bbc.com/news/[a-z]+-[a-z]*-*[a-z]*-*[a-z0-9]+/'
        )
        self.article_list = list(set(regex.findall(str(a[1]))))
        # note: there are (usually) two matches found by the first line,
        # the second of which should contain the script including all
        # relevant URLs.
            
            
            
class Euronews(Domain):
    """
    Class to handle http://www.euronews.com domain, includes site-specific
    HTML parsing.
    """

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

#===============================================================================
# Functions
#===============================================================================

def select_domains(how_many=None):
    """
    Retrieves the stored domains which are to be scraped from the database.
    Argument how_many limits the number of retrieved domains and is used 
    only for testing/debugging.
    """

    conn = sqlite3.connect('domain_db.db')
    cursor = conn.cursor()
    if how_many: 
        cursor.execute('SELECT * FROM domains LIMIT ?', (how_many, ))
    else:
        cursor.execute('SELECT * FROM domains')
    data = cursor.fetchall()
    conn.close()
    data = [tup for tup in data if tup[0] is not None]            
    return data

#===============================================================================
# Constants
#===============================================================================

DOMAIN_CLASSES = {'Al-Jazeera': AlJazeera,
                  'EUObserver': EUObserver,
                  'ArsTechnica': ArsTechnica,
                  'SPIEGEL Intl': SPIEGELIntl,
                  'BBC News': BBCNews,
                  'euronews': Euronews}    