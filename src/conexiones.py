import mysql.connector


def connection():
    try:
        database = mysql.connector.connect(host='localhost',
                                           database="HyBank",
                                           user='root',
                                           password='',
                                           raise_on_warnings=True)
        cursor = database.cursor(buffered=True)

        return [database, cursor]
    except:
        print("Base de datos inacesible")

