from dumps.Adapter import *

class MysqlAdapter(Adapter):
  def __init__(self):
    Adapter.__init__(self)
    self.username = 'mysql'
    self.sudoAsUsername = True
    self.excludedTables = ['mysql', 'information_schema']
    self.dumpDirectory  = '/home/dev/mysql_dumps/'
 

  def getDatabasesListCmd(self):
      return "mysql -u " + self.username + " -h " + self.host + " -p" + self.password + " --execute 'SHOW DATABASES;'  | awk 'NR > 1 { print $1 }' | " + self.getExcludesTablesString()


  def dump(self, dbName, nameStrategyFunction):
    pgDumpCommand = ''
    namePart      = nameStrategyFunction()
    if dbName != '':
      sqlFilePath   = self.dumpDirectory + "dump-" + dbName + "-" + namePart + ".sql"
      mysqlDumpCommand = "mysqldump  -u " + self.username +" -h " + self.host + " -p" + self.password + " " + dbName + " > " + sqlFilePath     
      print  'Execute mysqldump command ' + mysqlDumpCommand + ' ' + commands.getoutput(mysqlDumpCommand)
      print  'Execute gzip on ' + sqlFilePath + ' ' + commands.getoutput('gzip ' + sqlFilePath)
    
      return sqlFilePath + '.gz'
