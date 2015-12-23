"""
I am currently in the process of refactoring the main() function from main.py
into several classes, including the KeywordExtractor and Engine classes, to 
make the code cleaner and more readable. 

As is obvious, the KeywordExtractor class is currently only a placeholder.
"""

#===============================================================================
# Imports
#===============================================================================

from parallelprocessor import ParallelProcessor

#===============================================================================
# Class definition
#===============================================================================

class KeywordExtractor(ParallelProcessor):

  def __init__(self):
    super(KeywordExtractor, self).__init__()

  def look_for_keywords(self, keywords, to_process_q, processed_q):
    """
    Scans the text of the article objects in to_process_q for the keywords
    passed through the keywords argument.
    """
    pass

  def extract_keywords(self, to_process_q, processed_q):
    """
    Uses nltk library to extract most pertinent/relevant keywords from the
    article object texts.
    """
    pass