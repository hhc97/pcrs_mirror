import pickle
import psycopg2
import sys
from data import UserCounter

users, nextuser = pickle.load(open("users.pckl", "rb"))
inv_users = {v: k for k, v in users.items()}    # Assumes that user mapping is 1-1


conn = psycopg2.connect(database='csc108', user='fixit')

infile = open('top_n_questions_for_users.pkl', 'rb')
rec_data = pickle.load(infile)
infile.close()

dbCursor = conn.cursor() # opening conenction to db

sqlInsertRow = sqlInsertRow = "INSERT INTO public.fixit_problemrecommendedfixit(problem_type, problem_id, user_id ) VALUES(%s, %s, %s)" # query, inserting into fixit

for rec_problem in rec_data:
    # problem type, pid, uid
    try:
        rec_problem[2] = inv_users[rec_problem[2]]
    except KeyError:
        print(f"User not found: {rec_problem[2]}", file=sys.stderr)
        continue
    dbCursor.execute(sqlInsertRow, rec_problem)

conn.commit()
