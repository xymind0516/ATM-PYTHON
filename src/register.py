import conexiones
import hashlib
import datetime
import time
import random

connect = conexiones.connection()
db = connect[0]
cursor = connect[1]


class register():
    def __init__(self, username, apellido, passwd, email, DNI, TLF):
        self.username = username
        self.passwd = passwd
        self.apellido = apellido
        self.email = email
        self.DNI = DNI
        self.TLF = TLF

    def new_account(self):

        try:
            BALANCE: float = 1200.0
            ccv = random.randint(1000, 9999)
            IBAN = random.randint(1000000, 2000000)
            hash_element = hashlib.sha256()
            hash_element.update(self.passwd.encode('utf-8'))

            query = "INSERT INTO clients VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
            values = self.username, self.apellido, hash_element.hexdigest(), self.email, self.DNI, IBAN, self.TLF, ccv, BALANCE
            cursor.execute(query, values)
            db.commit()
            db.close()

            validation = cursor.fetchone()

            if validation is not None:
                return validation

            else:
                return 0

        except Exception as e:
            return e


#test = register("h", "h", "h", "h", "h", 2)
#test.new_account()

"""+---------------+--------------+------+-----+---------+----------------+
| id_cliente    | int          | NO   | PRI | NULL    | auto_increment |
| username      | varchar(200) | NO   |     | NULL    |                |
| lastname      | varchar(200) | NO   |     | NULL    |                |
| passwd        | varchar(254) | NO   |     | NULL    |                |
| email         | varchar(200) | NO   | UNI | NULL    |                |
| DNI           | varchar(10)  | NO   | UNI | NULL    |                |
| IBAN          | varchar(15)  | NO   | UNI | NULL    |                |
| TLF           | int          | NO   |     | NULL    |                |
| SECRET_NUMBER | int          | NO   |     | NULL    |                |
| BALANCE       | float(9,2)   | YES  |     | NULL    |                |
| fecha         | date         | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+-------------
"""