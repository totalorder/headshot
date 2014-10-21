# encoding: utf-8
import jaydebeapi
import os

DATABASES = {
    'dev': 'jdbc:oracle:thin:aimdev/ockelbo300@172.29.96.111:1521/AIMTST',
    'tst': 'jdbc:oracle:thin:aim/ockelbo300@172.29.96.111:1521/AIMTST',
    'prd': 'jdbc:oracle:thin:aim/ockelbo300@axsaimdbprd.int.axstores.se:1521/AIMPRD',
}


def createDatabaseConnection(environment):
    conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver',
                              [DATABASES[environment]],
                              os.path.join(os.path.abspath(os.path.dirname(__file__)), '../ojdbc6.jar'))
    conn.jconn.setAutoCommit(False)
    return conn
