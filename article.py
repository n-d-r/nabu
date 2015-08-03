# -*- coding: utf-8 -*-

import requests  
import time
from bs4 import BeautifulSoup

class Article:
    def __init__(self, url, domain_url):
        self.url   = url
        self.title = ''
        self.found_keywords = []
        self.domain_url = domain_url
    
    def __str__(self):
        return self.title + ' | ' + self.url + ' | ' + ', '.join(self.found_keywords)
        
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
        return(None)  
        
    def get_article_text(self):
        r = self._requests_wrapper(self.url)
        if r == None:
            return None
        else:
            soup = BeautifulSoup(r.text)
            
            try:
                self.title, self.text = self.extract_text(soup)
            except TypeError:
                return
    
    def scan_text(self, keywords):
        text_stripped = ''.join([char for char in self.text if \
            char not in '\'.,()[]{}\"'])
        text_split = text_stripped.split()
        for kw in keywords:
            if kw in text_split:
                self.add_keyword(kw)
        self.found_keywords = list(set(self.found_keywords))
                
    def add_keyword(self, keyword):
        self.found_keywords.append(keyword)         
        
    
class EUObserverArticle(Article):
    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'EU Observer'
    
    def extract_text(self, soup):
        title = soup.title.text.replace('\'', '')
        all_ps = soup.find('div', 'body larger').find_all('p')
        text = ' '.join([p.text for p in all_ps])
        return title, text
            
            
class AlJazeeraArticle(Article):  
    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'Al-Jazeera'

    def extract_text(self, soup):
        text = soup.find(id='article-body').text.replace('\n', ' ')
        title = soup.find_all(attrs={'class': 
                'heading-story'})[0].text.replace('\'', '')
        return title, text                        
                        
                        
class ArsTechnicaArticle(Article):
    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'Ars Technica'

    def extract_text(self, soup):
        title = soup.title.text.replace(' | Ars Technica', '')
        text = soup.find('article').find(id='article-guts').text.replace('\n', 
            ' ').replace('\xa0', ' ')  
        return title, text                
    
    
    
class SPIEGELIntlArticle(Article):
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
    def __init__(self, url, domain_url):
        Article.__init__(self, url, domain_url)
        self.domain = 'euronews'
        
    def extract_text(self, soup):
        title = ''.join([char for char in soup.title.text[0:(soup.title.text.index('|')-1)]])
        text = soup.find(id='articleTranscript').text.replace('\n', ' ')
        return title, text
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    