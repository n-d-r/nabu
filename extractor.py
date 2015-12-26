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

  def _lf(self, keywords, text):
    found_keywords = []
    text_stripped = ''.join(
      [char for char in text if char not in '\'.,()[]{}\"']
    )
    text_split = text_stripped.split()
    for keyword in keywords:
      if keyword in text_split:
        found_keywords.append(keyword)
    return list(set(found_keywords))

  def _look_for(self, to_process_q, processed_q, **kwargs):
    while not to_process_q.empty():
      article_object = to_process_q.get()
      article_object.found_keywords = self._lf(kwargs['keywords'], 
                                               article_object.text)
      processed_q.put(article_object)

  def look_for_keywords(self, keywords, to_process_q, processed_q):
    """
    Scans the text of the article objects in to_process_q for the keywords
    passed through the keywords argument.
    """
    self.execute(
      function=self._look_for,
      to_process_q=to_process_q,
      processed_q=processed_q,
      keywords=keywords
    )

  def extract_keywords(self, to_process_q, processed_q):
    """
    Uses nltk library to extract most pertinent/relevant keywords from the
    article object texts.
    """
    pass