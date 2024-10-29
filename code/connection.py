import pymysql

def get_connection():
    try:
        return pymysql.connect(
            host ='localhost',
            user = 'root',
            password= 'password',
            db='Airbnb'
        )
    except Exception as ex:
        print('Exception:{}'.format(str(ex)))

