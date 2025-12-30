import pymysql

# Use PyMySQL as a drop-in replacement for MySQLdb on Windows
# This allows the project to use the existing `django.db.backends.mysql`
# engine without needing to compile `mysqlclient`.
pymysql.install_as_MySQLdb()

