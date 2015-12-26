class ArgumentValidator(object):

  def __init__():
    pass

  @staticmethod
  def validate(input, target_type, startswith=None, 
               endswith=None, contains=None):
    if isinstance(target_type, list) or isinstance(target_type, tuple):
      if not any(isinstance(input, t) for t in target_type):
        raise Exception('"{}" is not of any acceptable type "{}"'.format(input, 
                        ', '.join([str(t) for t in target_type])))
    else:
      if not isinstance(input, target_type):
        raise Exception('"{}" is not of type "{}"'.format(input, target_type))

    if startswith:
      if not input.startswith(startswith):
        raise Exception('"{}" does not start with "{}"'
                        .format(input, startswith))
    elif endswith:
      if not input.endswith(endswith):
        raise Exception('"{}" does not end with "{}"'
                        .format(input, endswith))
    elif contains:
      if not contains in input:
        raise Exception('"{}" does not contain "{}"'
                        .format(input, contains))
    else:
      return True