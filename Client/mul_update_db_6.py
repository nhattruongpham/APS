import pymysql.cursors
import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

def Mul_UpdateDB_6(_db, _table, _col1, _val1, _col2, _val2, _col3, _val3):
    query = "UPDATE %s.%s SET %s = %s, %s =%s WHERE %s = %s", [_db, _table, _col1, _val1, _col2, _val2, _col3, _val3]
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except:
        connection.rollback()