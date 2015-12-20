# -*- coding: utf-8 -*-

"""
This file contains classes to provide functionality to store and process
data from individual news articles, as well as functions related to handling
such objects.
"""

#===============================================================================
# Imports
#===============================================================================

import requests  
import time
from bs4 import BeautifulSoup

#===============================================================================
# Class definitions
#===============================================================================

class Article:
    """
    Base class, provides basic functionality for processing of articles.
    Each object instance should represent one article from a particular
    news website. In successive steps and between the various queues from
    multiprocessing, more information is added to the article object at
    every step. All domain-specific classes inherit from this Article 
    base class.
    """

    def __init__(self, url, domain_url):
        self.url = url
        self.title = ''
        self.found_keywords = []
        self.domain_url = domain_url
    
    def __str__(self):
        return (self.title + ' | ' + self.url + ' | ' + 
                ', '.join(self.found_keywords))
        
    def extract_text(self, soup):
        print('[!] function should not ba called on Article base class')        
        raise SystemExit(0)        
        
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
        
    def get_article_text(self):
        r = self._requests_wrapper(self.url)
        if not r:
            return None
        else:
            soup = BeautifulSoup(r.text)
            try:
                self.title, self.text = self.extract_text(soup)
            except TypeError:
                return
    
    def scan_text(self, keywords):
        text_stripped = ''.join(
            [char for char in self.text if char not in '\'.,()[]{}\"']
        )
        text_split = text_stripped.split()
        for kw in keywords:
            if kw in text_split:
                self.add_keyword(kw)
        self.found_keywords = list(set(self.found_keywords))
                
    def add_keyword(self, keyword):
        self.found_keywords.append(keyword)         
        
        
    
class EUObserverArticle(Article):
    """
    Class to hold articles from http://euobserver.com, handles site-specific
    HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'EU Observer'
    
    def extract_text(self, soup):
        title = soup.title.text.replace('\'', '')
        all_ps = soup.find('div', 'body larger').find_all('p')
        text = ' '.join([p.text for p in all_ps])
        return title, text
            
            

class AlJazeeraArticle(Article):  
    """
    Class to hold articles from http://http://aljazeera.com/.com, handles
    site-specific HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'Al-Jazeera'

    def extract_text(self, soup):
        text = soup.find(id='article-body').text.replace('\n', ' ')
        title = soup.find_all(attrs={'class': 
                'heading-story'})[0].text.replace('\'', '')
        return title, text                        
                        

                        
class ArsTechnicaArticle(Article):
    """
    Class to hold articles from http://arstechnica.com/, handles site-specific
    HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'Ars Technica'

    def extract_text(self, soup):
        title = soup.title.text.replace(' | Ars Technica', '')
        text = soup.find('article').find(id='article-guts').text.replace('\n', 
            ' ').replace('\xa0', ' ')  
        return title, text                
    
    
    
class SPIEGELIntlArticle(Article):
    """
    Class to hold articles from http://www.spiegel.de, handles site-specific
    HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'SPIEGEL Intl'
        
    def extract_text(self, soup):
        title = soup.title.text.replace(' - SPIEGEL ONLINE', '')
        all_ps = soup.find(attrs={'class': 
            'article-section clearfix'}).find_all('p')
        text = ''
        for p in all_ps:
            text += str(p)
        text = text.replace('<p>', ' ').replace('</p>', 
               ' ').replace('\n', ' ').replace('<b>', ' ').replace('</b>', ' ')
        return title, text
    
    
    
class BBCNewsArticle(Article):
    """
    Class to hold articles from http://www.bbc.com/news, handles site-specific
    HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'BBC News'
        
    def extract_text(self, soup):
        title = soup.title.text.replace(' - BBC News', '')
        text = ''
        all_ps = soup.find(attrs={'class':'story-body__inner'}).find_all('p')
        for p in all_ps:
            text += p.text
        return title, text
    
    
    
class EuronewsArticle(Article):
    """
    Class to hold articles from http://www.euronews.com, handles site-specific
    HTML parsing.
    """

    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'euronews'
        
    def extract_text(self, soup):
        title = ''.join(
            [char for char in soup.title.text[0:(soup.title.text.index('|')-1)]]
        )
        text = soup.find(id='articleTranscript').text.replace('\n', ' ')
        return title, text

#===============================================================================
# Functions related to Article objects
#===============================================================================

def insert_article(article_obj):
    """
    Expects an article object as input and attempts to insert the data
    into the database. If it encounters an OperationalError or IntegrityError,
    instead of failing hard, it will print to console that the error occured.
    """

    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO artls(title, url, domain, domain_url, date, time) \
             VALUES(?, ?, ?, ?, date(), time())', 
             (article_obj.title, article_obj.url, article_obj.domain,
              article_obj.domain_url)
        )
        if len(article_obj.found_keywords) > 0:                
            for keyword in article_obj.found_keywords:
                cursor.execute('INSERT INTO artls_tags(artl_url, tag) \
                                VALUES(?, ?)', (article_obj.url, keyword))            
    except sqlite3.OperationalError:
        print('OperationalError')        
    except sqlite3.IntegrityError:
        print('IntegrityError: ' + article_obj.__str__() + '\n')                        
    conn.commit()                           
    conn.close()        