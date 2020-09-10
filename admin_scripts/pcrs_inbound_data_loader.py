import psycopg2
import sys

conn = psycopg2.connect(database='pcrs', host="pcrsdev.utm.utoronto.ca", user='waf', password='hehexd') #put pw here

infile = open('top_n_questions_for_users.pkl', 'rb')
rec_data = pickle.load(infile)
infile.close()

dbCursor = conn.cursor() # opening conenction to db

sqlInsertRow = "INSERT INTO fixit_problemrecommendedfixit values(%s, %s, %s, %s)" # query, inserting into fixit

for rec_problem in rec_data:
    # problem type, pid, uid
    dbCursor.execute(sqlInsertRow, rec_data)

conn.commit()







