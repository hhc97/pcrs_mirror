import psycopg2
import sys

conn = psycopg2.connect(database='csc108', user='fixit')

infile = open('top_n_questions_for_users.pkl', 'rb')
rec_data = pickle.load(infile)
infile.close()

dbCursor = conn.cursor() # opening conenction to db

sqlInsertRow = sqlInsertRow = "INSERT INTO public.fixit_problemrecommendedfixit(problem_type, problem_id, user_id ) VALUES(%s, %s, %s)" # query, inserting into fixit

for rec_problem in rec_data:
    # problem type, pid, uid
    dbCursor.execute(sqlInsertRow, rec_problem)

conn.commit()
