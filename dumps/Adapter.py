import commands, string, re

class Adapter:
  def __init__(self):
    self.username = 'dbuser'
    self.host     = 'localhost'
    self.password = 'secretpass'
    self.dbList          = []
    self.dumpDirectory   = '/home/dev/dumps'
    self.excludedTables  = []

  def getDatabasesListCmd(self):
    raise TypeError("Cannot call abstract method")
  

  def getExcludesTablesString(self):
    excludedTables = []
    for table in self.excludedTables:
      excludedTables.append('grep -v ' + table)
    return ' | '.join(excludedTables)
  
  def getDatabasesList(self):
    self.__prepareDatabasesList()
    return self.dbList

  def __prepareDatabasesList(self):
    if ([] == self.dbList):
      self.dbList = string.split(commands.getoutput(self.getDatabasesListCmd()), "\n");
      pattern = re.compile(r"^[A-Za-z]{1}[A-Za-z0-9_\-]+$")
      for dbName in self.dbList:
        if (None == pattern.match(dbName)):
          self.dbList.remove(dbName)
 
  def dump(self, dbName, nameStrategyFunction):
    raise TypeError("Cannot call abstract method")

  def configure(self, dict):
    for key, value in dict.iteritems():
      try:
        setattr(self, key, value)
      except AttributeError:
        print 'Configuration key not found ' + key
