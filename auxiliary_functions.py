# -*- coding: utf-8 -*-

import sqlite3

def select_domains(how_many=None):
    # how_many argument limits number of retrieved domains;
    # used only for testing/debugging
    conn = sqlite3.connect('domain_db.db')
    cursor = conn.cursor()
    if how_many: 
        cursor.execute('SELECT * FROM domains LIMIT ?', (how_many,))
    else:
        cursor.execute('SELECT * FROM domains')
    data = cursor.fetchall()
    conn.close()
    for tup in data:
        if tup[0] == None:
            del data[data.index(tup)]
    return data
    
def check_q_content(q):
    # for debugging
    while not q.empty():
        obj = q.get()
        print(obj)
    print('q empty')


def insert_article(article_obj):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO artls(title, url, domain, \
                                          domain_url, date, time) \
                        VALUES(?, ?, ?, ?, date(), time())', 
                        (article_obj.title, article_obj.url, article_obj.domain,
                        article_obj.domain_url))
        if len(article_obj.found_keywords) > 0:                
            for keyword in article_obj.found_keywords:
                cursor.execute('INSERT INTO artls_tags(artl_url, tag) \
                                VALUES(?, ?)', (article_obj.url, keyword))            
    except sqlite3.OperationalError:
        # to make sure that db is closed even if inserting fails
        print('OperationalError')        
#        conn.commit()
#        conn.close()  
    except sqlite3.IntegrityError:
        print('IntegrityError: ' + article_obj.__str__() + '\n')
#        conn.commit()
#        conn.close()                          
    conn.commit()                           
    conn.close()