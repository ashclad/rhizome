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

  def _invert(self):
    # TODO: Write code for exchanging the values of path-related v.
    # trail-related attr and moving center attribute's value into trail
    # attr
    trailmax = self._trailmax
    trails = self._trails
    trailposit = self._trlposition

    pathlist = []
    for p in self._pathmax:
      getattr(self, 'path' + str(p)).sort(key = lambda x: x._pthposition, reverse = True)
      # TODO: use mapping function to get elements of each path to have their
      # _pthposition be in accordance with their position in the path
      # for e in getattr(self, 'path' + str(p)):
      #   pass
      pathlist.append(getattr(self, 'path' + str(p)))
      pathlist.sort(key = lambda x: len(x), reverse = True)

    self._nodeid = pathlist[0]._nodeid
    self._content = pathlist[0]._content
    del pathlist[0]

    self._trailmax = self._pathmax
    self._trails = self._paths
    setattr(self, '_sharedtrail', self._sharedpath)
    self._trlposition = self._pthposition

    self._pathmax = trailmax
    self._paths = trails
    delattr(self, '_sharedpath')
    self._pthposition = trailposit

  def append(self, path, node):
    if not isinstance(path, int):
      raise TypeError(custerr.standardTypeMessage('path', path, int))

    if isinstance(node, Node):
      if hasattr(self, 'path' + str(path)) and path <= len(self._paths):
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
      for e in range(len(coll) - 1):
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

  def pop(self, path):
    currentpath = getattr(self, 'path' + str(path))

    currentpath[-1]._trailmax = None
    currentpath[-1]._trails = None
    currentpath[-1]._trlposition = None
    currentpath[-1].trail0 = None

    currentpath[-1]._nodeid -= 1
    delattr(currentpath[-1], '_sharedpath')
    currentpath[-1]._center = None
    trashed = currentpath[-1]
    del currentpath[-1]

    return trashed

  def attach(self, node, path = None):
    if isinstance(node, Node):
      self._pathmax += 1
      self._paths = range(0, self._pathmax)
      if path is None:
        path = len(self._paths) - 1
      setattr(self, 'path' + str(path), [])

      self.append(path, node)
    else:
      raise TypeError(custerr.standardTypeMessage('node', node, Node))

  def detach(self, path = None, forced = True):
    self._pathmax -= 1
    self._paths = range(0, self._pathmax)
    if path is None:
      path = len(self._paths)
    trashed = self.pop(path)
    leftover = getattr(self, 'path' + str(path))

    if forced:
      if trashed is not None:
        delattr(self, 'path' + str(path))
    else:
      if trashed is not None and len(trashed._paths) < 1:
        delattr(self, 'path' + str(path))
      else:
        raise RuntimeError('You cannot remove a path ' + \
        'that still contains nodes or is initial path.' + \
        ' Rerun until after all nodes are removed for ' + \
        'non-initial path.')

    return leftover

  def __len__(self):
    return len(self._gather())

  def __getitem__(self, key):
    return self._gather()[key]

  def __setitem__(self, key, val):
    # TODO: Add support for tupled keys
    if not isinstance(val, Node):
      currentpath = getattr(self, 'path' + str(key))
      currentpath[0].content = val
      val = [currentpath[0]]
      setattr(self, 'path' + str(key), val)
    else:
      self.detach(key)
      self.attach(val, key)

  def __delitem__(self, key):
    # TODO: Add support for tupled keys
    self.detach(key)

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

node = Node()
# print(node.next)
node_text = Node("text")
node_num = Node(1)
node_func = Node(26)
node.append(0, node_text)
node.append(0, node_num)
node.attach(node_func)
# node._move('f')
# print(node.next)
# node.detach()
# print(node.next)
