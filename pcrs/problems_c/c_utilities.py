from hashlib import sha1
from re import finditer, search
import logging


'''
Convert code with tags like [student], [blocked] and [hidden] from the starter_code by merging with the user_submission
'''
def process_code_tags(problem_id, user_submission, starter_code):
    #if code from editor, just return straight code
    if (str)(problem_id) == "9999999":
        logger.info("IN HERE PID IS CORRECT")
        if len(user_submission) == 0:
            raise Exception("No code found!")
        else:
            logger.info("length of sub is not 0")
            return user_submission
    else:
        # Get student code hashed key
        student_code_key = sha1(str(problem_id).encode('utf-8')).hexdigest()
        student_code_key_list = [m.start() for m in finditer(student_code_key, user_submission)]
        student_code_key_len = len(student_code_key)
        student_code_key_list_len = len(student_code_key_list)

        # Could not find student code
        if len(student_code_key_list) == 0 or len(student_code_key_list) % 2 != 0:
            raise Exception("No student code found!")

        # Get student code from submission and add it to the official exercise (from the database)
        student_code_list = []
        while len(student_code_key_list) >= 2:
            student_code_list.append(
                user_submission[student_code_key_list[0]+student_code_key_len+1: student_code_key_list[1]])
            del student_code_key_list[0], student_code_key_list[0]

        # Create variable mod_submission to handle the fusion of student code with starter_code from the database
        mod_submission = starter_code
        last_tag_size = len('[/student_code]') + 1
        for student_code in student_code_list:
            mod_submission = mod_submission[: mod_submission.find('[student_code]')] + \
                                    '\r\n' + student_code + '' +\
                                    mod_submission[mod_submission.find('[/student_code]')+last_tag_size:]

        # Replace hashed key with text (Implementation start/end)
        x = 0
        while x < student_code_key_list_len:
            m = search(student_code_key, user_submission)
            user_submission = user_submission[: m.start()] + user_submission[m.end():]
            x += 1

        # Remove blocked tags from the source code
        mod_submission = mod_submission.replace("[blocked]\r\n", '').replace("[/blocked]\r\n", '')
        mod_submission = mod_submission.replace("[blocked]", '').replace("[/blocked]", '')

        # Remove hidden tags from the source code
        mod_submission = mod_submission.replace("[hidden]\r\n", '').replace("[/hidden]\r\n", '')
        mod_submission = mod_submission.replace("[hidden]", '').replace("[/hidden]", '')


    return mod_submission


'''
Replace preprocessor directives with empty lines to allow pycparser to parse the file correctly
'''
def remove_preprocessor_directives(user_script):
    lines = user_script.split('\n')
    new_lines = [clear_directive_line(l) for l in lines]
    new_user_script = '\n'.join(new_lines)

    return new_user_script


def clear_directive_line(line):
    if ('_Generic' in line) or ('#include' in line):
        return '\r'
    else:
        return line
