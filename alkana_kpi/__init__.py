import pymysql

# Use PyMySQL as a drop-in replacement for MySQLdb on Windows
# This allows the project to use the existing `django.db.backends.mysql`
# engine without needing to compile `mysqlclient`.
pymysql.install_as_MySQLdb()
import MySQLdb
# Mock version for Django compatibility (mysqlclient 2.2.7)
setattr(MySQLdb, 'version_info', (2, 2, 7, 'final', 0))
setattr(MySQLdb, '__version__', '2.2.7')

