from statistics import mean as avg
import custerr

class Node:
  def __init__(self, content = None):
    # Below identifies a central/parent node for future linked nodes
    self._center = None
    # Below gives unique number for node on graph
    self._nodeid = 0
    # Below specifies what branch/edge/link of the central/parent node one is on
    self._pathmax = 1
    self._paths = range(0, self._pathmax)
    self._sharedpath = None
    self._trailmax = None
    self._trails = None
    # Below specifies what position node is in, in a specific branch/edge/link
    self._pthposition = 0
    self._trlposition = None
    if content:
      self.content = content
    self.path0 = []
    self.trail0 = None

  def append(self, path, node):
    if not isinstance(path, int):
      raise TypeError(custerr.standardTypeMessage('path', path, int))

    if isinstance(node, Node):
      if hasattr(self, 'path' + str(path)) and path in self._paths:
        node._center = self

        node._sharedpath = path
        node._nodeid += 1

        currentpath = getattr(self, 'path' + str(path))
        node._pthposition = len(currentpath)
        currentpath.append(node)
        currentpath[-1]._trailmax = 1
        currentpath[-1]._trails = range(0, currentpath[-1]._trailmax)
        currentpath[-1]._trlposition = 0
        currentpath[-1].trail0 = [self]
        setattr(self, 'path' + str(path), currentpath)
      else:
        raise custerr.PathError(path)
    else:
      raise TypeError(custerr.standardTypeMessage('node', node, Node))

  def _move(self, dir = 'f'):
    result = []

    if dir == 'f':
      coll = self._paths
      id = 'path'
    elif dir == 'b':
      coll = self._trails
      id = 'trail'
    else:
      raise ValueError()

    if len(coll):
      for e in coll:
        currentattr = getattr(self, id + str(e))
        if len(currentattr):
          result.append(currentattr[0])

    return tuple(result)

  @property
  def next(self):
    return self._move('f')

  @property
  def prev(self):
    return self._move('b')

  def _gather(node, dir = 'f'):
    if dir == 'f':
      id = 'path'
    elif dir == 'b':
      id = 'trail'
    else:
      raise ValueError()

    if isinstance(node, Node):
      trav_from_node = []

      num = 0
      while hasattr(node, id + str(num)):
        trav_from_node.append(getattr(node, id + str(num)))
        num += 1
      else:
        return trav_from_node

  def pop(path):
    currentnode = getattr(self, 'path' + str(path))

    currentnode[-1]._trailmax = None
    currentnode[-1]._trails = None
    currentnode[-1]._trlposition = None
    currentnode[-1].trail0 = None

    # TODO: Get currentnode[-1] path attrs and create new self path attrs
    # with them starting at self path attr amount or 1 less--make sure all trail
    # info is replaced for nodes of each currentnode[-1] path attr

    currentnode[-1]._nodeid = 0
    delattr(currentnode, '_sharedpath')
    currentnode[-1]._center = None

    return currentnode[-1]

  def attach(self, node):
    self._pathmax += 1
    self._paths = range(0, self._pathmax)
    path = self._paths[-1]
    setattr(self, 'path' + str(path), [])

    self.append(path, node)

  def detach(self):
    # Code likely to make use of class's pop method
    pass

  def __repr__(self):
    strrepr = '*|'

    # TODO: Validate insides of sequence/iterable types
    if self.content:
      if isinstance(self.content, str):
        strrepr += '"' + self.content + '"'
      elif isinstance(self.content, (int,float,complex)):
        strrepr += '(' + str(self.content) + ')'
      elif isinstance(self.content, (list,tuple,range)):
        strrepr += type(self.content).__name__ + '<?>'
      elif isinstance(self.content, dict):
        strrepr += type(self.content).__name__ + '<keys:?>'
      else:
        strrepr += type(self.content).__name__
    else:
      strrepr += self._nodeid

    strrepr += ' -> ' + str(self._paths)

    return strrepr

class Graph:
  pass
