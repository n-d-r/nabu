"""
I am currently in the process of refactoring the main() function from main.py
into several classes, including the KeywordExtractor and Engine classes, to 
make the code cleaner and more readable. 

The Engine class will do most of the heavy lifting that is currently part of
the main() function in main.py
"""

#===============================================================================
# Imports
#===============================================================================

import sqlite3

from multiprocessing import Process, Manager
from extractor import KeywordExtractor
from parallelprocessor import ParallelProcessor
from validator import ArgumentValidator
from domains import DOMAIN_CLASSES

#===============================================================================
# Class definition
#===============================================================================

class Engine(ParallelProcessor):

  def __init__(self, keywords, article_database, domain_database):
    super(Engine, self).__init__()

    # multiprocessing infrastructure
    self.manager = Manager()
    self.domain_q = self.manager.Queue()
    self.article_q = self.manager.Queue()
    self.scan_q = self.manager.Queue()
    self.processed_q = self.manager.Queue()

    ArgumentValidator.validate(
      article_database, target_type=str, endswith='.db'
    )
    self.article_database = article_database

    ArgumentValidator.validate(
      domain_database, target_type=str, endswith='.db'
    )
    self.domain_database = domain_database

    if keywords:
      ArgumentValidator.validate(keywords, target_type=list)
      self.keywords = keywords

  def process_keywords(self, to_process_q, processed_q):
    extractor = KeywordExtractor()
    if self.keywords:
      extractor.look_for_keywords(
        keywords=self.keywords,
        to_process_q=self.to_process_q,
        processed_q=self.processed_q
      )
    else:
      extractor.extract_keywords(
        to_process_q=self.to_process_q,
        processed_q=self.processed_q
      )

  def _select_domains(self, how_many=None):
      """
      Retrieves the stored domains which are to be scraped from the database.
      Argument how_many limits the number of retrieved domains and is used 
      only for testing/debugging.
      """
      conn = sqlite3.connect(self.domain_database)
      cursor = conn.cursor()
      if how_many: 
          cursor.execute('SELECT * FROM domains LIMIT ?', (how_many, ))
      else:
          cursor.execute('SELECT * FROM domains')
      data = cursor.fetchall()
      conn.close()
      data = [tup for tup in data if tup[0] is not None]            
      return data

  def load_domains(self, how_many=None):
    domain_tuples = self._select_domains(how_many)
    domains = [DOMAIN_CLASSES[name](url) for url, name in domain_tuples]
    for domain in domains:
      self.domain_q.put(domain)

  def _insert_keyword(url, keyword):
    command = """
      INSERT INTO artls_tags(artl_url, tag)
      VALUES ("{}", "{}")
    """
    data = [url, keyword]
    self.cursor.execute(command.format(*data))

  def _insert(article_object):
    command = """
      INSERT INTO artls(title, url, domain, domain_url, date, time)
      VALUES("{}", "{}", "{}", "{}", date(), time())
    """
    data = [article_object.title, article_object.url, 
            article_object.domain, article_object.domain_url]
    self.cursor.execute(command.format(*data))
    for keyword in article_object.found_keywords:
      self._insert_keyword(article_object.url, keyword)

  def insert_articles(to_process_q):
    self.conn = sqlite3.connect(self.article_database)
    self.cursor = conn.cursor()
    while not to_process_q.empty():
      try:
        article_object = to_process_q.get()
        ArgumentValidator.validate(article_object, target_type=Article)
        self._insert(article_object)
      except sqlite.IntegrityError:
        print('IntegrityError: {}\n'.format(article_object))
      except sqlite3.OperationalError:
        print('OperationalError: {}\n'.format(article_object))
    self.conn.commit()
    self.conn.close()