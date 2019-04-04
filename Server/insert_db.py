import pymysql.cursors
import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

def InsertDB(_db, _table, _col1, _val1, _col2, _val2):
    query = "INSERT INTO %s.%s (%s, %s) VALUES (%s, %s)", (_db,_table, _col1,_val1, _col2, _val2)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except:
        connection.rollback()