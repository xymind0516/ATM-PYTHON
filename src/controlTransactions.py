import conexiones
connect = conexiones.connection()
db = connect[0]
cursor = connect[1]


class Control(object):
    def __init__(self, dni_c, type_t, quanty_t, destine_t):
        self.dni_c = dni_c
        self.type_t = type_t
        self.quanty_t = quanty_t
        self.destine_t = destine_t


    def save_transactions(self):

        try:
            sql = "INSERT INTO Transact (id_transc, DNI_C, type, quanty, destine, fecha) VALUES (NULL,%s, %s, %s, %s, CURDATE())"
            values = self.dni_c, self.type_t, self.quanty_t, self.destine_t
            cursor.execute(sql, values)
            db.commit()
            validation = cursor.fetchone()
            return validation

        except Exception as e:
            return e



#test = Control('h', 'query',  100, 'admin')
#test.save_transactions()

""" +-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id_transc | int          | NO   | PRI | NULL    | auto_increment |
| DNI_C     | varchar(10)  | NO   | MUL | NULL    |                |
| type      | varchar(20)  | NO   |     | NULL    |                |
| quanty    | float(9,2)   | NO   |     | NULL    |                |
| destine   | varchar(200) | NO   |     | NULL    |                |
| fecha     | date         | NO   |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+"""