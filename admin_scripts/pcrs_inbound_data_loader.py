import psycopg2
import sys
import pickle
from datetime import date

# csc108 is real
# 108clone is test
conn = psycopg2.connect(database='108clone', user='fixit')

infile = open('top_n_questions_for_users.pkl', 'rb')
rec_data = pickle.load(infile)
infile.close()

dbCursor = conn.cursor() # opening conenction to db

sqlInsertRow = sqlInsertRow = "INSERT INTO public.fixit_problemrecommendedfixit(problem_type, problem_id, user_id, date ) VALUES(%s, %s, %s, %s)" # query, inserting into fixit

for rec_problem in rec_data:
    # problem type, pid, uid
    rec_problem += (date.today(),)
    dbCursor.execute(sqlInsertRow, rec_problem)

conn.commit()
