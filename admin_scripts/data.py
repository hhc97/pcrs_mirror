import pickle

training_set_ids = ['13345', '13619', '13688', '12815', '12744', '13570', '13632', '12992', '13057', '14019', '13414', '13145', '13289', '13378', '13021', '12825', '13327', '13123', '13766', '12923', '13775', '13504', '13579', '12832', '12804', '13399', '13519', '13731', '13755', '16910', '13116', '13495', '13171', '13635', '13745', '13469', '12855', '12977', '13347', '13765', '12918', '13423', '13258', '13356', '13616', '12978', '13048', '13322', '13587', '13492', '13405', '13160', '12824', '13379', '13685', '17020', '12890', '13211', '13790', '13203', '13139', '12901', '13434', '12847', '12916', '12865', '13369', '13431', '13476', '13572', '12733', '13234', '13219', '13182', '13131', '13657', '13088', '12827', '14854', '13466', '13401', '13767', '17062', '13103', '13084', '13650', '13080', '13163', '13416', '12809', '13776', '12795', '13633', '13142', '13357', '13249', '12911', '17008', '13674', '13035', '13676', '12945', '12967', '12872', '13365', '13659', '13704', '13100', '13062', '13437', '13639', '13395', '13213', '15948', '14287', '13121', '13736', '13554', '13273', '12956', '13441', '13156', '13155', '12853', '13746', '13760', '13697', '12957', '13756', '13388', '13473', '13371', '13481', '13679', '13524', '13625', '13629', '12777', '12867', '13764', '13614', '13217', '13530', '13551', '12731', '13785', '12974', '17063', '13305', '13143', '13046', '13791', '13003', '13364', '12961', '12950', '13283', '13686', '13071', '12887', '13227', '13119', '17057', '13725', '13149', '12770', '13732', '13501', '13503', '13338', '12884', '13571', '13718', '13453', '13267', '12793', '13482', '13607', '13675', '12940', '13518', '13271', '13262', '13771', '13360', '13397', '12737', '13513', '13538', '13212', '12962', '13419', '13134', '13710', '13186', '13636', '13205', '13670', '13297', '13341', '13307', '13185', '12740', '12850', '13787', '12987', '13250', '12821', '17011', '13362', '13284'] 

######### CLASSES

class UserCounter():
    def __init__(self):
        self.next = 0

class PyProblem(object):
    def __init__(self, id, challenge_id, name, description, starter_code, max_score, **args):
        self.problem_id = id
        self.challenge_id = challenge_id
        self.description = description
        self.starter_code = starter_code
        self.max_score = max_score
        self.name = name
        self.tags = []
        self.quest_name = None
        self.quest_description = None
    def add_tag(self, tag_name):
        self.tags.append(tag_name)
    def add_quest(self, name, description, **args):
        self.quest_name = name
        self.quest_description = description

class PySubmission(object):
    def __init__(self, id, user_id, problem_id, timestamp, score, has_best_score, **args):
        self.submission_id = id
        self.user_id = user_id
        self.problem_id = problem_id
        self.timestamp = timestamp
        self.score = score
        self.has_best_score = has_best_score

class MCOption(object):
    def __init__(self, id, answer_text, is_correct):
        self.option_id = id
        self.answer_text = answer_text
        self.is_correct = is_correct
    def __str__(self):
        return str((self.answer_text, self.is_correct),)
    def __repr__(self):
        return str(self)

class MCProblem(object):
    def __init__(self, id, challenge_id, description, name, **args):
        self.problem_id = id
        self.challenge_id = challenge_id
        self.description = description
        self.name = name
        self.options = {} # dictionary values are MCOption objects
        self.tags = []
        self.quest_name = None
        self.quest_description = None
    def add_tag(self, tag_name):
        self.tags.append(tag_name)
    def add_option(self, id, answer_text, is_correct, **args):
        self.options[id] = MCOption(id, answer_text, is_correct)
    def add_quest(self, name, description, **args):
        self.quest_name = name
        self.quest_description = description
    def __str__(self):
        return str((self.problem_id, self.name, self.tags, self.description),)
    def __repr__(self):
        return str(self)

class MCSubmissionOption(object):
    def __init__(self, id, was_selected, is_correct, **args):
        self.id = id
        self.was_selected = was_selected
        self.is_correct = is_correct

class MCSubmission(object):
    def __init__(self, id, user_id, problem_id, timestamp, **args):
        self.submission_id = id
        self.user_id = user_id
        self.problem_id = problem_id
        self.timestamp = timestamp
        self.options = {} # Whether each option was selected
    def add_option(self, option_id, **args):
        self.options[option_id] = MCSubmissionOption(**args)
    def is_correct(self):
        return all(option.is_correct for option in self.options)

######### DATA LOADING FUNCTIONS

def load_py_problems():
    # Dictionary where the 
    #  keys = problem id
    #  values = PyProblem object
    return pickle.load(open("/home/fixit/py_problems.pkl", "rb"))

def load_all_py_submissions():
    return pickle.load(open("/home/fixit/py_submissions.pkl", "rb"))
    
def load_py_test_submissions():
    """Load python problems from test set
    20% of total dataset"""
    return pickle.load(open("/home/fixit/py_test_data.pkl", "rb")) 

def load_py_submissions():
    """Load python problems from training set
    80% of total dataset"""
    # List of PySubmission objects
    return pickle.load(open("/home/fixit/py_training_data.pkl", "rb"))

def pickle_mc():
    a = pickle.load(open("/home/fixit/mc_submissions.pkl", "rb"))
    b = a.copy()
    l = {}
    j = {}
    for i in b.keys():
        if b[i].user_id in training_set_ids:
            l[i] = b[i]
        else:
            j[i] = b[i]
    pickle.dump(l, open("/home/fixit/mc_test_data.pkl", "wb"))
    pickle.dump(j, open("/home/fixit/mc_train_data.pkl", "wb"))

def load_all_mc_submissions():
    return pickle.load(open("/home/fixit/mc_submissions.pkl", "rb"))

def load_mc_problems():
    # Dictionary where the 
    #  keys = problem id
    #  values = MCProblem object
    return pickle.load(open("/home/fixit/mc_problems.pkl", "rb"))

def load_mc_submissions():
    # List of MCSubmission objects
    return pickle.load(open("/home/fixit/mc_train_data.pkl", "rb"))

def load_mc_test_submissions():
    return pickle.load(open("/home/fixit/mc_test_data.pkl", "rb"))  
