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

from multiprocessing import Process, Manager
from extractor import KeywordExtractor
from parallelprocessor import ParallelProcessor

#===============================================================================
# Class definition
#===============================================================================

class Engine(ParallelProcessor):

  def __init__(self, keywords):
    super(Engine, self).__init__()

    # multiprocessing infrastructure
    self.manager = Manager()
    self.domain_q = self.manager.Queue()
    self.article_q = self.manager.Queue()
    self.scan_q = self.manager.Queue()
    self.processed_q = self.manager.Queue()
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

  def prepare_domains(self, domains):
    for domain in domains:
      self.domain_q.put(domain)