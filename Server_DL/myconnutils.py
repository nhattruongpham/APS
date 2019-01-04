import pymysql 


# Hàm trả về một connection.
def getConnection():
    # Bạn có thể thay đổi các thông số kết nối.
    connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='Truong@1996', database='ParkingSlot')
    return connection