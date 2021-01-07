import conexiones

connect = conexiones.connection()
db = connect[0]
cursor = connect[1]


class login():

    def __init__(self, DNI, passwd):
        self.DNI = DNI
        self.passwd = passwd

    def login_user(self):
        try:
            query = "SELECT DNI, passwd FROM clients WHERE DNI = %s AND passwd = %s"
            values = self.DNI, self.passwd

            cursor.execute(query, values)
            validation = cursor.fetchone()

            if validation:
                return validation

            else:
                return 0

        except Exception as e:
            return e

