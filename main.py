# -*- coding: utf-8 -*-

#===============================================================================
# Imports
#===============================================================================

from multiprocessing import Process, Manager  

from articles import (Article, EUObserverArticle, AlJazeeraArticle,
                      ArsTechnicaArticle, SPIEGELIntlArticle, BBCNewsArticle, 
                      EuronewsArticle, insert_article)
from domains import (Domain, AlJazeera, EUObserver, ArsTechnica, SPIEGELIntl,
                     BBCNews, Euronews, select_domains, DOMAIN_CLASSES)
from worker_functions import (retrieve_article_urls, retrieve_article_text,
                              scan_article_text)

#===============================================================================
# main() below
#===============================================================================

def main():
    
    # parsing command-line arguments
    print('Parsing arguments...')
    import argparse
    parser = argparse.ArgumentParser()
    group  = parser.add_mutually_exclusive_group()
    
    group.add_argument('-f', '--keywords-from-file', 
                        help='specify file from which to read keywords. default: \
                        \'keywords.txt\'')
                        
    group.add_argument('-u', '--keywords-from-user', 
                        help='specify keywords directly; separate keywords \
                        by commata. do NOT use spaces.')
                        
    parser.add_argument('-a', '--ask', action='store_true',
                        help='flag whether python should ask for every article \
                        first before inserting in database.')
    
    args = parser.parse_args()
    
    ask_before_inserting = args.ask
    print('Finished parsing arguments.\n')
    
    # loading keywords
    print('Loading keywords...')
    if args.keywords_from_file:
        with open(args.keywords_from_file, 'r') as f:
            flines = f.readlines()
            keywords = [kw.strip('\n') for kw in flines]
    elif args.keywords_from_user:
        keywords = args.keywords_from_user.split(',')
    else:
        keywords = None
    print('Finished loading keywords.\n')
    
    # constants
    NUM_MAX_PROCESSES = 10

    # setting up multiprocessing infrastructure
    print('Setting up multiprocessing infrastructure...')
    manager     = Manager()
    domain_q    = manager.Queue()
    article_q   = manager.Queue()
    scan_q      = manager.Queue()
    processed_q = manager.Queue()
    print('Finished setting up multiprocessing infrastructure.\n')

    # retrieving saved domains and domain URLs
    print('Retrieving domains and domain URLs...')

    domain_tuples = select_domains(how_many=1)
#    domain_tuples = select_domains()
    domains = [DOMAIN_CLASSES[name](url) for url, name in domain_tuples]
    
    for domain in domains:
        domain_q.put(domain)
    print('Finished retrieveing domains and domain URLs.\n')
         
        
    # extracting article URLs from domains/frontpages
    print('Extracting article URLs from domains/frontpages...')
    url_processes = []
    for p in range(NUM_MAX_PROCESSES):
        url_processes.append(Process(target = retrieve_article_urls,
                                     args   = (domain_q, article_q)))
                                     
    for process in url_processes:
        process.start()
    for process in url_processes:
        process.join()
    print('Finished extracting article URLs.\n')
         

    # extracting text of individual articles
    print('Extracting text from individual articles...')    
    text_processes = []
    for p in range(NUM_MAX_PROCESSES):
        text_processes.append(Process(target = retrieve_article_text,
                                      args   = (article_q, scan_q)))
                                      
    for process in text_processes:
        process.start()
    for process in text_processes:
        process.join()         
    print('Finished extracting text from individual articles.\n')                

    
    # scanning individual article texts for keywords
    if keywords:
        print('Scanning individual article texts for keywords...')
        scan_processes = []
        for p in range(NUM_MAX_PROCESSES):
            scan_processes.append(Process(target = scan_article_text,
                                          args   = (scan_q, processed_q, keywords)))
                                          
        for process in scan_processes:
            process.start()
        for process in scan_processes:
            process.join()
        print('Finished scanning individual articles.\n')
    else:
        print('Shifting articles from scan_q to processed_q...')
        while not scan_q.empty():
            article_obj = scan_q.get()
            processed_q.put(article_obj)
        print('Finished shifting.\n')
        

    print('Inserting relevant articles into database...')        
    while not processed_q.empty():
        article_obj = processed_q.get()
        if keywords:
            if len(article_obj.found_keywords) > 0:
                if ask_before_inserting:
                    print(article_obj)
                    print('Insert? [y/n]')
                    while True:
                        insert = input('> ')
                        if insert in 'yY':
                            insert_article(article_obj)
                            break
                        elif insert in 'nN':
                            break
                        else:
                            print('invalid input. choose Y or N')
                else:
                    insert_article(article_obj)
        else:
            if ask_before_inserting:
                    print(article_obj)
                    print('Insert? [y/n]')
                    while True:
                        insert = input('> ')
                        if insert in 'yY':
                            insert_article(article_obj)
                            break
                        elif insert in 'nN':
                            break
                        else:
                            print('invalid input. choose Y or N')
            else:
                insert_article(article_obj)
    print('Finished inserting relevant articles into database.\n')
     
    
if __name__ == '__main__':
    main()