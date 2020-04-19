# import psycopg2


# class Database():
#     cursor = None

#     def __init__(self, config):
#         self.conn = psycopg2.connect(
#             host=config['POSTGRES']['HOST'],
#             port=config['POSTGRES']['PORT'],
#             database=config['POSTGRES']['DATABASE'],
#             user=config['POSTGRES']['USER'],
#             password=config['POSTGRES']['PASSWORD']
#         )
#         self.cursor = self.conn.cursor()

#     def query(self, query):
#         self.cursor.execute(query)

#     def close(self):
#         self.cursor.close()
#         self.conn.close()
