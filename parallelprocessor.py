"""
The ParallelProcessor class is simply there to be inherited from by the
Engine and KeywordExtractor classes that both need the execute() method.
"""

#===============================================================================
# Imports
#===============================================================================

from multiprocessing import Process

#===============================================================================
# Class definition
#===============================================================================

class ParallelProcessor(object):

  def __init__(self):
    self.NUM_MAX_PROCESSES = 5

  def execute(self, function, to_process_q, processed_q, **kwargs):
    processes = []
    for p in range(self.NUM_MAX_PROCESSES):
      processes.append(Process(target=function,
                               args=(to_process_q, processed_q),
                               kwargs=kwargs))

    for process in processes: process.start()
    for process in processes: process.join()