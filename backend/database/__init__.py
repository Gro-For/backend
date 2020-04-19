import psycopg2


class Database():
    __conn = None

    def __init__(self, config):
        try:
            print(
                config['POSTGRES']['HOST'],
                config['POSTGRES']['PORT'],
                config['POSTGRES']['DATABASE'],
                config['POSTGRES']['USER'],
                config['POSTGRES']['PASSWORD']
            )
            self.__conn = psycopg2.connect(
                host=config['POSTGRES']['HOST'],
                port=config['POSTGRES']['PORT'],
                dbname=config['POSTGRES']['DATABASE'],
                user=config['POSTGRES']['USER'],
                password=config['POSTGRES']['PASSWORD']
            )

            return True
        except psycopg2.OperationalError:
            return "База данных не доступна"

    def __connect(self, config):
        pass

    def select_data(self, query):
        cursor = self.__conn.cursor()
        execute = cursor.execute(query)
        cursor.close()
        return execute.fetchall()

    def insert_data(self, insert):
        cursor = self.__conn.cursor()
        cursor.execute(query)
        cursor.close()
        return True

    def close(self):
        self.__conn.close()
