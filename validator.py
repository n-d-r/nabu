class ArgumentValidator(object):

  def __init__():
    pass

  @staticmethod
  def validate(input, type, startswith=None, endswith=None, contains=None):
    if not isinstance(input, type):
      raise Exception('"{}" is not of type "{}"'.format(input, type))
    elif startswith:
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