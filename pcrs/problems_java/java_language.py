import sys
import os
import shutil
import subprocess
import tempfile
import re
from datetime import datetime

from pcrs.settings import PROJECT_ROOT
from problems.pcrs_languages import BaseLanguage


class CompilationError(Exception):
    pass


class JavaSpecifics(BaseLanguage):
    ''' Representation of Java language:
        * string encoding in visualizer format,
        * generation of execution trace for visualizer,
        * running tests

        TODO: no visualizer support currently provided
              see http://www.pythontutor.com/java.html#mode=edit
              for a tool that could be used to provide support
    '''

    temp_path = PROJECT_ROOT + "/languages/java/execution/temporary/"
    jvm_res_path = PROJECT_ROOT + "/languages/java/execution/resources/"

    def __init__(self, *args, **kwargs):
        BaseLanguage.__init__(self, *args, **kwargs)
        self.compiled = False
        self.testSuiteClassName = None
        self.tempdir = None

    def encode_str(self, target_value):
        ''' Encode string target_value in visualizer format.
        '''
        raise NotImplementedError("Visualization not yet supported")

    def get_exec_trace(self, user_script, add_params):
        ''' Get execution trace of string user_script providing additional parameters.
        '''
        raise NotImplementedError("Visualization not yet supported")

    def run_test_suite(self):
        ''' Return dictionary ret containing results of a testrun.
            ret has the following mapping:
            'test_val' -> encoded for visualizer format test output.
            'passed_test' -> boolean
            'exception' (only if exception occurs) -> exception message.
        '''
        ret = {
            'failures': {},
            #'exception': None
        }
        if not self.compiled:
            ret['exception'] = "Code could not be compiled before test execution"
            return ret

        try:
            flags = " ".join([
                "-Djava.security.manager=default",
                "-Djava.security.policy={0}pcrs.policy".format(self.jvm_res_path),
                self._createDependencyFlagString(),
                "org.junit.runner.JUnitCore", # run our test through JUnit
            ])
            proc = subprocess.Popen(
                    "java {0} {1}".format(flags, self.testSuiteClassName),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self.tempdir,
                    shell=True,
                    universal_newlines=True)
            output, err = proc.communicate(timeout=8) # 8 second timeout on run
        except subprocess.TimeoutExpired as e:
            try:
                proc.kill()
            except:    # May already have terminated or been killed
                pass
            ret['exception_type'] = 'error'
            ret['exception'] = "Timeout expired: do you have an infinite loop?"
        except Exception as e:
            print(e)
            raise
        else:
            reg = (
                '\d+\) ([\w_]+).*?\n' # Capture failed method name
                '(.+?)(?:\s*at {0})'  # Capture stack trace only in student code
            ).format(self.testSuiteClassName)
            for m in re.findall(reg, output, re.DOTALL):
                methodName = m[0]
                stackTrace = self._steralizeStackTrace(m[1])
                ret['failures'][methodName] = stackTrace
        return ret

    def compile(self, user, user_files, test_code, deny_warning=False):
        ''' Compile the given user code, raising a compile error if unable.
        '''
        if self.compiled:
            return

        # From this point on, we need to delete the tempdir if there is a failure.
        try:
            self.tempdir = tempfile.mkdtemp(
                    prefix="{0}-{1}-".format(user, datetime.now().strftime('%m%d-%H:%M:%S'), dir=self.temp_path),
                    dir=self.temp_path)

            for f in user_files:
                self._compileSource(f['code'], fileName=f['name'])

            self._compileSource(test_code, isTestCode=True)
            self.compiled = True
        except Exception as e:
            self.clear()
            raise # reraise

    def _compileSource(self, source_code, fileName=None, isTestCode=False):
        ''''Compiles given source code into the temporary run directory.

        Args:
            source_code: The raw source code to compile
            fileName:    The file to compile to - defaults to the public class
            isTestCode:  If this is test code, it will be more
                         cautious with error message information.
        Raises:
            CompilationError: On failure
        '''
        if not fileName:
            className = re.search('public\s+class\s+(\w+)', source_code).group(1)
            fileName = '{0}.java'.format(className)

            if isTestCode: # Used to determine which file to run
                self.testSuiteClassName = className

        source_path = "{0}{1}{2}".format(self.tempdir, os.sep, fileName)
        with open(source_path, "w") as f:
            f.write(source_code)

        # Actual compilation
        try:
            flags = self._createDependencyFlagString()
            proc = subprocess.Popen(
                    'javac {0} {1}'.format(flags, fileName),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self.tempdir,
                    shell=True,
                    universal_newlines=True)
            output, err = proc.communicate(timeout=8) # 8 second timeout on run
        except subprocess.CalledProcessError as e:
            raise CompilationError("javac failed with:\n" + str(e.output))
        except TimeoutExpired:
            try:
                proc.kill()
            except:
                pass # If it is already dead
            raise CompilationError('Compilation timeout expired. Please try again')

        if err:
            if isTestCode:
                err = self._stripTestCodeCompileError(err)
            raise CompilationError(err)

    def _createDependencyFlagString(self):
        dependencies = [ 'junit-4.12.jar', 'hamcrest-core-1.3.jar' ]
        classpath = ":".join([self.jvm_res_path + d for d in dependencies])
        # We need '.' in the classpath to load student class files
        return "-cp .:" + classpath

    def _steralizeStackTrace(self, trace):
        '''Ensures no JUnit errors are exposed to the student. Instead, this
           will strip out the assertion message or return a blank string.
        '''
        m = re.search("(?:org\.junit\.\w+|java\.lang\.AssertionError):? ?(.*)", trace)
        if m:
            message = m.group(1).strip()
            # The instructor didn't provide a message, so this should be hidden
            if message.startswith('expected:'):
                return ''
            return message
        return trace

    def _stripTestCodeCompileError(self, error):
        '''Strips important compile errors from test code compile issues

        Args:
            error: The error message (from javac)
        Returns:
            A nicely stripped error message, not exposing the test case code.
        '''
        if re.search('cannot find symbol', error):
            messages = set()
            for m in re.findall('\s*symbol:\s*\w+\s*([\w_]+)', error):
                messages.add("You must define '{0}' as described.".format(m))
            return '\n'.join(messages)

        m = re.search('error: non\-static (?:method|variable) ([\w_]+\(?\)?)', error)
        if m:
            return "You must define '{0}' as static.\n".format(m.group(1))

        m = re.search('error: ([\w_]+\(?\)?) has private access', error)
        if m:
            return "You must define '{0}' as public.\n".format(m.group(1))

        return error

    def clear(self):
        ''' Delete the executable and other files associated with this code.
        '''
        try:
            shutil.rmtree(self.tempdir)
        except OSError as e:
            pass
        self.compiled = False
        self.tempdir = None

    def get_download_mimetype(self):
        ''' Return string with mimetype.
        '''
        return 'application/x-java'

