from dumps.Adapter import *

class PostgresAdapter(Adapter):
  def __init__(self):
    Adapter.__init__(self)
    self.username = 'postgres'
    self.sudoAsUsername = True
    self.excludedTables = ['postgres', 'template0', 'template1']
    self.dumpDirectory  = '/home/dev/pg_dumps/'    

  def getDatabasesListCmd(self):
    return "sudo su " + self.username + " -c 'cd; psql -c \"\l\" |  awk \"NR > 3 { if (\\$1 != \\\"\\\" && \\$1 ~ \\\"^[A-Za-z0-9_\\\\-]\\\") { print \\$1 } } \" | " + self.getExcludesTablesString() + "'" 


  def dump(self, dbName, nameStrategyFunction):
    pgDumpCommand = ''
    namePart      = nameStrategyFunction()
    sqlFilePath   = self.dumpDirectory + "dump-" + dbName + "-" + namePart + ".sql"
    pgDumpCommand = "sudo su " + self.username + " -c 'cd; pg_dump " + dbName + " > " + sqlFilePath + "'"    
    print  'Execute pg_dump command ' + pgDumpCommand + ' ' + commands.getoutput(pgDumpCommand)
    print  'Execute gzip on ' + sqlFilePath + ' ' + commands.getoutput('gzip ' + sqlFilePath)    
    
    return sqlFilePath + '.gz'
