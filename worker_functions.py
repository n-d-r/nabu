# -*- coding: utf-8 -*-

def retrieve_article_urls(domain_q, article_q):
    while not domain_q.empty():
        domain = domain_q.get()
        domain.get_article_urls()
        for article_obj in domain.article_obj_generator():        
            article_q.put(article_obj)
    
    
def retrieve_article_text(article_q, scan_q):
    while not article_q.empty():
        article = article_q.get()
        article.get_article_text()
        scan_q.put(article)
        
        
def scan_article_text(scan_q, processed_q, keywords):
    while not scan_q.empty():
        article = scan_q.get()
        article.scan_text(keywords)
        processed_q.put(article)        