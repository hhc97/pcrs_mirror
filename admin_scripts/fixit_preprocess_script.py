import pickle
from data import PyProblem, PySubmission, MCOption, MCProblem, MCSubmissionOption, MCSubmission

######### DATABASE

def get_connection():
    import psycopg2 
    return psycopg2.connect("dbname='csc108' user='fixit'") # host='localhost'")

def generate_content(cur, query, key=None):
    cur.execute(query)
    rows = cur.fetchall()
    headers = [c.name for c in cur.description]
    for row in rows:
        yield dict(zip(headers, row))

def get_content(cur, query, key=None):
    cur.execute(query)
    rows = cur.fetchall()
    headers = [c.name for c in cur.description]

    if key:
        results = {}
        for row in rows:
            item = dict(zip(headers, row))
            results[item[key]] = item
    else:
        results = []
        for row in rows:
            item = dict(zip(headers, row))
            results.append(item)
    return results

def get_mc_problems(cur):
    query = "select * from problems_multiple_choice_problem;"
    return get_content(cur, query, "id")

def get_mc_tags(cur):
    query = "select * from problems_multiple_choice_problem_tags;"
    return get_content(cur, query)

def get_py_tags(cur):
    query = "select * from problems_python_problem_tags;"
    return get_content(cur, query)

#def get_mc_tags(cur):
#    query = "select * from problems_python_problem_tags;"
#    return get_content(cur, query)

def get_mc_options(cur):
    query = "select * from problems_multiple_choice_option;"
    return get_content(cur, query)

def generate_py_submissions(cur, sample=False):
    query = "select * from problems_python_submission"
    if sample:
        query += " limit 5000"
    return generate_content(cur, query)

def generate_mc_submissions(cur, sample=False):
    query = "select * from problems_multiple_choice_submission"
    if sample:
        query += " limit 5000"
    return generate_content(cur, query)

def generate_mc_submissions_options(cur, sample):
    query = "select * from problems_multiple_choice_optionselection"
    if sample:
        query += " limit 5000"
    return generate_content(cur, query)

def get_tags(cur):
    query = "select * from content_tag;"
    return get_content(cur, query, "id")

def get_python_problems(cur):
    query = "select * from problems_python_problem;"
    return get_content(cur, query, "id")

def get_content_challenges(cur):
    query = "select * from content_challenge;"
    return get_content(cur, query, "id")

def get_content_quest(cur):
    query = "select * from content_quest;"
    return get_content(cur, query, "id")


######### BUILD OBJECTS

def build_mc_problems(cur):
    # dictionary of challenges & quests
    content_challenges = get_content_challenges(cur)
    content_quest = get_content_quest(cur)

    # populate a dictionary of MCProblem, keyed by problem_id
    problems = {}
    for problem_id, obj in get_mc_problems(cur).items():
        problems[problem_id] = MCProblem(**obj)

        # add quest info
        challenge_id = obj['challenge_id']
        if challenge_id in content_challenges:
            quest_id = content_challenges[challenge_id]['quest_id']
            if quest_id:
                problems[problem_id].add_quest(**content_quest[quest_id])

    # populate tags in the problems dictionary
    tags = get_tags(cur)
    for obj in get_mc_tags(cur):
        problem_id = obj["problem_id"]
        tag_id = obj["tag_id"]
        tag_name = tags[tag_id]["name"]
        if problem_id in problems:
            problems[problem_id].add_tag(tag_name)

    # populate optionss
    for obj in get_mc_options(cur):
        problem_id =  obj['problem_id']
        problems[problem_id].add_option(**obj)
    return problems

def build_py_problems(cur):
    # dictionary of challenges & quests
    content_challenges = get_content_challenges(cur)
    content_quest = get_content_quest(cur)

    # start building the problems
    problems = {}
    for problem_id, obj in get_python_problems(cur).items():
        problems[problem_id] = PyProblem(**obj)

        # add quest info
        challenge_id = obj['challenge_id']
        if challenge_id in content_challenges:
            quest_id = content_challenges[challenge_id]['quest_id']
            if quest_id:
                problems[problem_id].add_quest(**content_quest[quest_id])

    # populate tags in the problems dictionary
    tags = get_tags(cur)
    for obj in get_py_tags(cur):
        problem_id = obj["problem_id"]
        tag_id = obj["tag_id"]
        tag_name = tags[tag_id]["name"]
        problems[problem_id].add_tag(tag_name)
    return problems

def build_mc_submissions(cur, sample, user_d):
    # get the submission ids and time stamps
    submissions = {}
    for obj in generate_mc_submissions(cur, sample):
        submission_id = obj['id']
        if obj["user_id"] not in user_d:
            continue # ignore this line
        obj['user_id'] = user_d[obj['user_id']]
        submissions[submission_id] = MCSubmission(**obj)

    # get the option selected
    found = 0
    not_found = 0
    for obj in generate_mc_submissions_options(cur, sample):
        submission_id = obj['submission_id']
        if submission_id not in submissions:
            # could be because we're sampling, and could be
            # because we're filtering out non-students
            not_found += 1
            continue
        else:
            submissions[submission_id].add_option(**obj)
            found += 1

    print("Total:", len(submissions))
    print("Found:", found)
    print("Not Found:", not_found)

    return submissions

def build_py_submissions(cur, sample, user_d):
    # get the submission ids and time stamps
    submissions = {}
    for obj in generate_py_submissions(cur, sample):
        submission_id = obj['id']
        if obj["user_id"] not in user_d:
            continue # ignore this line
        obj['user_id'] = user_d[obj['user_id']]
        submissions[submission_id] = PySubmission(**obj)
    return submissions

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()

    users = {student['username']: student['id'] for student in get_content(cur, "select id, username from users_pcrsuser where is_student")}
    fixit = get_content(cur, "select * from fixit_studentfixitprofile", "id")
    fixit_exclude = [(fixit[id]['problem_type'], fixit[id]['problem_id'], fixit[id]['user_id']) for id in fixit.keys()]
    pickle.dump(fixit_exclude, open("fixit_submissions.pkl", "wb"))
    
    short_answer = get_content(cur, "select * from problems_short_answer_submission")
    pickle.dump(short_answer, open("short_answers.pkl", "wb"))

    py_problems = build_py_problems(cur)
    pickle.dump(py_problems, open("py_problems.pkl", "wb"))

    mc_problems = build_mc_problems(cur)
    pickle.dump(mc_problems, open("mc_problems.pkl", "wb"))

    # only return a subset of the data
    sample = False 

    if sample:
        mc_submissions = build_mc_submissions(cur, sample, users)
        py_submissions = build_py_submissions(cur, sample, users)
    else:
        mc_submissions = build_mc_submissions(cur, sample, users)
        pickle.dump(mc_submissions, open("mc_submissions.pkl", "wb"))

        py_submissions = build_py_submissions(cur, sample, users)
        pickle.dump(py_submissions, open("py_submissions.pkl", "wb"))

    pickle.dump(users, open("users.pckl", "wb"))
