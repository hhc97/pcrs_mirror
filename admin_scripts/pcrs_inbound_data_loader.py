import psycopg2
import sys

conn = psycopg2.connect(database='pcrs', host="pcrsdev.utm.utoronto.ca", user='waf', password='hehexd') #put pw here

dbCursor = conn.cursor() # opening conenction to db

sqlInsertRow = "INSERT INTO fixit_problemrecommendedfixit values(%s, %s, %s, %s)" # query, inserting into fixit

# row id, problem type, pid, uid

dbCursor.execute(sqlInsertRow, (5, 'multiple_choice', 2, 1))

conn.commit()

# create a database in ur postgreql table.






