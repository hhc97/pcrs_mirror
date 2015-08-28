from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint

import json

from problems_c.c_language import *
from problems_c.c_utilities import *
from problems_c.models import Problem
import logging
import traceback

import pdb

@csrf_exempt
def visualizer_details(request):
    """
        Return json encoded dictionary ret containing trace required
        for visualizer. Contents of the ret depend on language implementation.
    """
    logger = logging.getLogger('activity.logging')

    ret = {}
    try:
        user_script = request.POST.get("user_script")

        # Get starter code from database and insert student submission
        problem_id = request.POST.get("problemId")

        starter_code = Problem.objects.get(pk=problem_id).starter_code

        clean_code = process_code_tags(problem_id, user_script, starter_code)

        # add_params is always JSON encoded.
        add_params = json.loads(request.POST.get("add_params"))
        add_params = dict(add_params)
        # Use CSRF_COOKIE as username
        add_params['user'] = request.META["CSRF_COOKIE"]

        # Create a language instance
        gen = CSpecifics(add_params['user'], clean_code, "[hidden]" in starter_code)

        print("GEN IS :")
        print(gen)
        #PROBLEM HERE---
        ret = gen.get_exec_trace(clean_code, add_params, [])

    except Exception as e:
        ret['exception'] = str(e)

    json_output = json.dumps(ret, indent=None)

    return HttpResponse(json_output)


def new_visualizer_details(request):
    """
        Return json encoded dictionary ret containing trace required
        for the new C visualizer.
    """
    logger = logging.getLogger('activity.logging')

    ret = {}
    try:
        user_script = request.POST.get("user_script")

        # Get starter code from database and insert student submission
        problem_id = request.POST.get("problemId")

        starter_code = Problem.objects.get(pk=problem_id).starter_code

        hidden_lines_list = get_hidden_lines(problem_id, user_script, starter_code)
        clean_code = process_code_tags(problem_id, user_script, starter_code)

        # add_params is always JSON encoded.
        add_params = json.loads(request.POST.get("add_params"))
        add_params = dict(add_params)
        # Use CSRF_COOKIE as username
        add_params['user'] = request.META["CSRF_COOKIE"]

        # Create a language instance
        gen = CSpecifics(add_params['user'], clean_code, hidden_lines_list == [])

        #PROBLEM HERE---
        ret = gen.get_exec_trace(clean_code, add_params, hidden_lines_list)

        if 'error' in ret:
            error = ret['error']
            exception_msg = ""
            if 'exception' in error:
                exception_msg = error['exception']
            elif 'runtime_error' in error:
                exception_msg = error['runtime_error']

            ret = { 'exception': exception_msg }

    except Exception as e:
        tb = e.__traceback__
        traceback.print_tb(tb)
        print(e)
        ret['exception'] = str(e)

    json_output = json.dumps(ret, indent=None)
    return HttpResponse(json_output)


    #REPLACE WITH THIS IF WE WANT TO HOOK IT UP TO A PREMADE JSON:
    # sample_json_file_dir = './languages/c/visualizer/pycparser-experimentation/sample_json_traces/'

    # # Load the sample JSON file
    # ret = {}
    # with open(sample_json_file_dir + 'asher-mockup.json') as data_file:
    #     ret = json.load(data_file)


    # json_output = json.dumps(ret, indent=None)
    # return HttpResponse(json_output)
