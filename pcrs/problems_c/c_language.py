import os
import subprocess
import datetime
from pcrs.settings import PROJECT_ROOT, USE_SAFEEXEC, SAFEEXEC_USERID, SAFEEXEC_GROUPID
from languages.c.visualizer.cg_stacktrace import CVisualizer


class CSpecifics():
    """ Representation of C language:
        * running tests
    """
    # Compilation status and flags
    compiled = False
    compilation_ret = {}
    # File name addendum
    date_time = str((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
    # Temporary directory path where the temporary C files and output files will be saved
    temp_path = PROJECT_ROOT + "/languages/c/execution/temporary/"
    # Username
    username = ""
    # Problem source code
    submission = ""

    def __init__(self, username, submission):
        self.username = username
        self.submission = submission

    def run_test(self, test_input, expected_output):
        """ Return dictionary ret containing results of a testrun.
            ret has the following mapping:
            'test_val' -> test output.
            'passed_test' -> boolean
            'exception' (only if exception occurs) -> exception message.
            'warning' (only if warning occurs) -> warning message.
        """

        ret = {}
        user = str(self.username)
        user_script = str(self.submission)

        # Compile C source code
        if not self.compiled:
            self.compilation_ret = self.compile_source_code(user, user_script)
        # Naming the temporary output file
        temp_output_file = self.temp_path + user + self.date_time + ".out"
        # Naming the temporary runtime error file
        # temp_runtime_error_file = self.temp_path + user + self.date_time + "_runtime_error.out"

        try:
            ret["exception_type"] = self.compilation_ret["exception_type"]
            ret["exception"] = self.compilation_ret["exception"]
            if self.compilation_ret["exception_type"] == "error":
                raise CompilationError

            # Test input and expected output data
            test_input = str(test_input)
            expected_output = str(expected_output)

            if USE_SAFEEXEC:
                # Safeexec path
                safe_exec = PROJECT_ROOT + "/languages/c/execution/safeexec_master/safeexec"

                # C safe execution parameters
                max_time_sec = "10"  # 10 seconds
                max_process_mem = "40960"  # 40 megabytes
                max_number_files = "20"  # 20 files -- need some runtime libraries
                max_file_size = "5120"  # 5 megabytes

                # Running C program in a secure environment
                process = subprocess.call(safe_exec + " -o " + temp_output_file + " -d " + max_process_mem
                                + " -U " + SAFEEXEC_USERID + " -G " # + " -e " + temp_runtime_error_file
                                + SAFEEXEC_GROUPID + " -T " + max_time_sec + " -F " + max_number_files
                                + " -f " + max_file_size + " -q " + self.compilation_ret["temp_gcc_file"]
                                + " " + test_input + " > /dev/null 2> /dev/null", shell=True)
            else:
                process = subprocess.call(self.compilation_ret["temp_gcc_file"] + " " + test_input + " > " + temp_output_file, shell=True)
                # + " 2> " + temp_runtime_error_file

            # Getting the execution output
            f = open(temp_output_file, 'r')
            execution_output = f.read()
            f.close()

            # Runtime error during process execution (desconsider warning errors)
            if process != 0 and ret["exception"] == " ":
                execution_output = 'Runtime error!'
                ret["exception_type"] = "warning"
                ret["exception"] = "Runtime error!<br />Please check your code for errors such as segmentation faults."

            # Getting the run time error output
            #f = open(temp_runtime_error_file, 'r')
            #runtime_error = f.read()
            #if runtime_error:
            #    print("===== safeexec runtime error=====\n", runtime_error, "==========")   # To system error log. Probably better to activity log.
            #f.close()

            # Remove escape sequences in case of a string instance
            if isinstance(expected_output, str):
                expected_output_tmp = expected_output.replace('\n', "").replace('\r', "").replace(" ", "")
            else:
                expected_output_tmp = expected_output

            # Remove escape sequences in case of a string instance
            if isinstance(execution_output, str):
                execution_output_tmp = execution_output.replace('\n', "").replace('\r', "").replace(" ", "")
            else:
                execution_output_tmp = execution_output

            ret["test_val"] = execution_output
            ret["passed_test"] = False if expected_output_tmp != execution_output_tmp else True

        except CompilationError:
            ret["passed_test"] = False
            ret["test_val"] = ret["exception"]

        except SyntaxError as e:
            ret["exception_type"] = 'error'
            ret["exception"] = str(e)
            ret['passed_test'] = False
            ret['test_val'] = str(e)

        except Exception as e:
            ret["exception_type"] = 'error'
            ret["exception"] = str(e)
            ret['passed_test'] = False
            ret['test_val'] = str(e)

        finally:
            # Deleting temporary files
            try:
                os.remove(temp_output_file)
            except OSError:
                pass
            #try:
            #    os.remove(temp_runtime_error_file)
            #except OSError:
            #    pass
            return ret

    def compile_source_code(self, user, user_script):

        # Naming the C file
        temp_c_file = self.temp_path + user + self.date_time + ".c"
        # Naming the file which the gcc creates
        temp_gcc_file = self.temp_path + user + self.date_time + ".o"
        # Naming the temporary error file
        temp_error_file = self.temp_path + user + self.date_time + "_error.out"
        # Compilation flags
        flags = "-Wall"

        ret = {"temp_gcc_file": temp_gcc_file}
        try:
            # Creating the C file
            f = open(temp_c_file, 'w')
            f.write(user_script)
            f.close()

            # Compiling the C file
            subprocess.call("gcc " + flags + " " + temp_c_file + " -o " + temp_gcc_file + " 2> " + temp_error_file,
                            shell=True)

            # Getting the error output to check if there were any compilation errors
            f = open(temp_error_file, 'r')
            compilation_alert = f.read()
            f.close()

            # Check compilation alerts (errors and warnings)
            if compilation_alert:
                # Removing the temporary path of the string
                compilation_alert = compilation_alert.replace(self.temp_path, "")
                # Removing the file name from the error string
                compilation_alert = compilation_alert.replace((user + self.date_time + ".c:"), '')
                # Check for compilation, or warning errors
                if not compilation_alert.find("warning") != -1:
                    ret["exception_type"] = "error"
                    ret["exception"] = str("Compilation Error:\n" + compilation_alert).replace('\n', '<br />')
                else:
                    ret["exception_type"] = "warning"
                    ret["exception"] = str("Compilation Warning:\n" + compilation_alert).replace('\n', '<br />')
            else:
                ret["exception_type"] = " "
                ret["exception"] = " "

        except Exception as e:
            ret["exception_type"] = "error"
            ret["exception"] = "Compilation Error\n"

        finally:
            # Check compilation flag
            self.compiled = True
            # Deleting temporary files
            try:
                os.remove(temp_c_file)
            except OSError:
                pass
            try:
                os.remove(temp_error_file)
            except OSError:
                pass
            return ret

    def clear_exec_file(self, file_location):
        try:
            os.remove(file_location)
        except OSError:
            pass
        self.compiled = False

    def get_exec_trace(self, user_script, add_params):
        """ Return dictionary ret containing all variables results.
            ret has the following mapping:
            'exception' (only if exception occurs) -> exception message.
            'trace' -> program trace.
        """

        user = add_params['user']
        temp_path = os.getcwd()
        test_input = add_params['test_case']

        # Compile code checking for invalid changes after submission
        ret = self.compile_source_code(user, user_script)

        # Remove compiled file
        self.clear_exec_file(ret["temp_gcc_file"])
        # Return compilation/warning error if it exists
        if 'exception' in ret:
            return {'trace': None, 'exception': ret["exception"]}

        c_visualizer = CVisualizer(user, temp_path)
        # Build initial stack with functions and variables data
        stack_trace = c_visualizer.build_stacktrace(user_script)
        # Change original source code with the proper printf (debug)
        mod_user_script = c_visualizer.change_code_for_debbug(stack_trace, user_script)
        # Compile and run the modified source code and remove compiled file
        code_output = self.run_test(user, mod_user_script, test_input, test_input)
        self.clear_exec_file(self.compilation_ret["temp_gcc_file"])
        # Get the proper encoding for the javascript visualizer
        visualizer_encoding = c_visualizer.get_visualizer_enconding(code_output, stack_trace, user_script)

        self.clear_exec_file(ret["temp_gcc_file"])
        return visualizer_encoding

    def get_download_mimetype(self):
        """ Return string with mimetype. """
        return 'text/x-c'


class CompilationError(Exception):
    pass
