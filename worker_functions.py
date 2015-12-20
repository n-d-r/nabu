# -*- coding: utf-8 -*-

"""
This file contains the worker functions that are mapped to the individual
processes from the multiprocessing module.
"""

def retrieve_article_urls(domain_q, article_q):
    """
    The domain_q contains the domain objects from which to retrieve individual 
    news articles. For every domain, the articles are extracted from the
    HTML with the respective domain-specific function. The newly created
    article objects are then put on the article_q.
    """

    while not domain_q.empty():
        domain = domain_q.get()
        domain.get_article_urls()
        for article_obj in domain.article_obj_generator():        
            article_q.put(article_obj)
    
    
def retrieve_article_text(article_q, scan_q):
    """
    The article_q contains article objects that were extracted from the 
    domains. The worker function triggers the extraction of the article
    text from the HTML. The text is then saved (as part of the 
    get_article_text() method) as an attribute of the article object.
    Finally, the processed article objects (now with text) are then placed
    on the scan_q.
    """

    while not article_q.empty():
        article = article_q.get()
        article.get_article_text()
        scan_q.put(article)
        
        
def scan_article_text(scan_q, processed_q, keywords):
    """
    The scan_q contains article objects with the extracted text. The worker
    function calls the respective article subclass method to scan for the 
    keywords which were passed through with the 'keywords' parameter. The
    scan_text() method saves the keywords found in the article object, which 
    is then placed on the processed_q. 
    """

    while not scan_q.empty():
        article = scan_q.get()
        article.scan_text(keywords)
        processed_q.put(article)        