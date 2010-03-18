def stampNameStrategy():
  from time import gmtime, strftime
  return strftime('%Y%m%d%H%M%S', gmtime())
