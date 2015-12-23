"""
I am currently in the process of refactoring the main() function from main.py
into several classes, including the KeywordExtractor and Engine classes, to 
make the code cleaner and more readable. 

The main() function in this file will eventually replace the one from main.py,
and will hopefully be much more readable and clean.
"""

#===============================================================================
# Imports
#===============================================================================

from worker_functions import (retrieve_article_urls,
                              retrieve_article_text)
from engine import Engine

#===============================================================================
# main() function
#===============================================================================

def main():

  import argparse
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()

  group.add_argument(
    '-f', '--keywords-from-file',
    help=('specify file from which to read keywrds. ' + 
          'default is "keywords.txt"')
  )

  group.add_argument(
    '-u', '--keywords-from-user',
    help=('specify keywords directly, separate by commata. ' +
          'do not use spaces.')
  )

  parser.add_argument(
    '-a', '--ask', action='store_true',
    help=('flag whether Python should ask for every article ' +
          'first before inserting it into the database.')
  )

  args = parser.parse_args()

  ask_before_inserting = args.ask

  if args.keywords_from_file:
    with open(args.keywords_from_file, 'r') as f:
      flines = f.readlines()
      keywords = [kw.strip('\n') for kw in flines]
  elif args.keywords_from_user:
    keywords = args.keywords_from_user.split(',')
  else:
    keywords = None

  domain_tuples = select_domains(how_many=3)
  domains = [DOMAIN_CLASSES[name](url) for url, name in domain_tuples]

  engine = Engine(keywords=keywords)
  engine.prepare_domains(domains=domains)
  engine.execute(
    function=retrieve_article_urls,
    to_process_q=engine.domain_q,
    processed_q=engine.article_q
  )
  engine.execute(
    function=retrieve_article_text,
    to_process_q=engine.article_q,
    processed_q=engine.scan_q
  )
  engine.process_keywords(
    to_process_q=engine.scan_q,
    processed_q=engine.processed_q
  )

  # To be continued...