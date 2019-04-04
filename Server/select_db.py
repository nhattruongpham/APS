import pymysql.cursors
import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

def SelectDB(_colsec, _db, _table, _col1, _val1):
    query = "SELECT %s FROM %s.%s WHERE %s = %s",(_colsec, _db, _table, _col1, _val1)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            # result = cursor.fetchall()
            result = cursor.fetchone()
            connection.commit()
    except:
        connection.rollback()
    # for row in result:
    #     for col in row:
    #         selected = col
    return result#,selected