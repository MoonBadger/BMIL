import psycopg2


class DBManager:
    err_flag = False

    @staticmethod
    def connect():
        return psycopg2.connect(dbname='postgres', user='moonbadger',
                                password='14012003', host='localhost')

    @staticmethod
    def select(call):
        try:
            conn = DBManager.connect()
            cursor = conn.cursor()
            cursor.execute(call)
            answer = cursor.fetchall()
            cursor.close()
            conn.close()
            DBManager.err_flag = False
            return answer
        except:
            DBManager.err_flag = True
            return None


    @staticmethod
    def change(call):
        try:
            conn = DBManager.connect()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(call)
            cursor.close()
            conn.close()
            DBManager.err_flag = False
            return True
        except:
            DBManager.err_flag = True
            return False
