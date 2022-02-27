# ERROR MESSAGE FUNCTIONS
# ------
def standardTypeMessage(param, obj, altopts = []):
  err = True

  if isinstance(param, str):
    err = False

  if err:
    raise TypeError(standardTypeMessage('param', param))
  else:
    errmess = 'argument for parameter "' + param + '" of invalid type '
    errmess += type(obj).__name__

    if altopts:
      helpstr = '; must be of type '

      if isinstance(altopts, (tuple,list,range)):
        isvalid = True
        helpstr_end = ''

        if len(altopts) == 2:
          if hasattr(altopts[0], '__name__'):
            opts1 = altopts[0].__name__
          else:
            opts1 = altopts[0]

          if hasattr(altopts[1], '__name__'):
            opts2 = altopts[1].__name__
          else:
            opts2 = altopts[1]

          helpstr_end += opts1 + ' or ' + opts2
        else:
          altopts = altopts[:-1]
          lastopt = altopts[-1]

          for opt in altopts:
            if isinstance(opt, str):
              helpstr_end += opt + ', '
              continue
            elif hasattr(opt, '__name__'):
              helpstr_end += opt.__name__ + ', '
              continue
            else:
              isvalid = False
              break

        if isvalid:
          if len(altopts) > 2:
            helpstr_end += 'or ' + lastopt
          helpstr += helpstr_end
      elif isinstance(altopts, str):
        helpstr += altopts
      elif hasattr(altopts, '__name__'):
        helpstr += altopts.__name__
      else:
        raise TypeError(standardTypeMessage('altopts', altopts))

  return errmess + helpstr

def standardValueError(param, val, allowed = []):
  pass

# CUSTOM ERROR CLASSES
# ------
pathdefault = 'no such path extends from node'
class PathError(KeyError):
  def __init__(self, path = None, cntxt = None, message = pathdefault):
    self.target_path = path
    self.source_node = cntxt
    self.message = message

    if self.target_path and self.source_node:
      instcheck = (isinstance(path, str) and isinstance(cntxt, str))
      if instcheck:
        self.message = 'there is no path ' + path + \
        ' extending from node ' + cntxt
      else:
        self.message = 'there is no path ' + str(path) + \
        ' extending from node ' + cntxt
    elif self.target_path:
      instcheck = (isinstance(path, str) and isinstance(cntxt, str))
      if instcheck:
        self.message = 'there is no path ' + path + ' extending from node'
      else:
        self.message = 'there is no path ' + str(path) + ' extending from node'
    super().__init__(self.message)
