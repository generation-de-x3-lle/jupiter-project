import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="root",
    password="password")
cur = conn.cursor()
#cur.execute('SELECT * FROM test_table')
#names = cur.fetchmany()
print('PostgreSQL database version:')
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)
#print(names)
cur.close()
conn.close()