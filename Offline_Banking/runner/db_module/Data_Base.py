import sqlite3
from runner.db_module.TestDatabase import Register_DB as td
class DataBaseFile:

    def __init__(self,file_name):
        self.file_name = file_name

    def get_connection(self):
        con = sqlite3.connect(self.file_name)
        print('Create Connection')
        return con

    def create_table(self,con,table_name):
        con.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name+
                    '''(F_Name TEXT NOT NULL,
                       L_Name TEXT NOT NULL,
                       EMAIL TEXT NOT NULL,
                       PWD TEXT NOT NULL)'''
                    )
        print('Created Table')



    def insert_records(self, con, table_name, obj):
        data = ''' INSERT INTO ''' + table_name + '''('F_name','L_name', 'Email', 'Pwd')
                   VALUES(?, ?, ?, ?)'''
        con.execute(data, (obj.f_name, obj.l_name, obj.email, obj.pwd))
        con.commit()
        print('inserted records')

    def close_connect(self,con):
        con.close()
        print('Database closed')

if __name__ == "__main__":
    db_obj = DataBaseFile('demo_123.db')
    con = db_obj.get_connection()
    db_obj.create_table(con,'register')
    db_obj.insert_records(con, "register", obj)
    #db_obj.close_connection(con)
    #obj = Register_DB(f_name = 'balaji', l_name ='m',email = 'balaji@gmail.com',pwd = '123')
    #db_obj.insert_records(con,"register",obj)
