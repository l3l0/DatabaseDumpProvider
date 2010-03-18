from dumps.Adapter import *
import commands

class DumpProvider:
  """Database Dump Class"""
  def __init__(self, dbAdapter):
    if not isinstance(dbAdapter, Adapter):
      raise TypeError, "Dump class needs DbAdapter class"
    self.dbAdapter = dbAdapter
    self.filePaths = []
    self.sshLogin = 'dump'
    self.sshPort  = '22'
    self.sshHost  = 'somehost'
    self.sshDumpLocalization = '/home/dump/dumps'
    self.maxDumpsPerDatabase = 2

  def createDumps(self, namingStrategyFunction):
    for db in self.dbAdapter.getDatabasesList():
      filePath = self.dbAdapter.dump(db, namingStrategyFunction)
      self.filePaths.append(filePath)

  def sendToServer(self):
    for filePath in self.filePaths:
     if filePath:
       print 'Coping ' + filePath + ' into ' + self.sshHost 
       commands.getoutput('scp -P ' + self.sshPort + ' ' + filePath + ' ' + self.sshLogin + '@' + self.sshHost + ':' + self.sshLocalization)
  
  def configure(self, dict):
    for key, value in dict.iteritems():
      setattr(self, key, value)
    self.dbAdapter.configure(dict)

  def removeOldDumpFiles(self):
    import os
    import fnmatch
 
    files = os.listdir(self.dbAdapter.dumpDirectory)
    files.sort()
    files.reverse()   
 
    for dbName in self.dbAdapter.getDatabasesList():
      index = 0
      for fileName in files:
        if fnmatch.fnmatch(fileName, 'dump-' + dbName  + '*.sql.gz'):
          if (index > self.maxDumpsPerDatabase - 1):
            os.remove(self.dbAdapter.dumpDirectory + fileName)
            print 'Remove dump file: ', self.dbAdapter.dumpDirectory + fileName
          index = index + 1
  
  def run(self, stampNameStrategy):
    self.createDumps(stampNameStrategy)
    self.sendToServer()
    self.removeOldDumpFiles()
          
   
    
