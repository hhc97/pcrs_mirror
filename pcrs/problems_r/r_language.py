<<<<<<< HEAD
import os
<<<<<<< HEAD
=======
import subprocess
import sys
>>>>>>> pcrs-r: implemented rpy2
=======
>>>>>>> updated requirements.txt
from rpy2 import robjects
from hashlib import sha1
from datetime import datetime

import problems.pcrs_languages as languages

<<<<<<< HEAD
R_TEMPPATH = os.path.join("languages/r/CACHE/")
=======
R_STATICFILES = "" ### PATH TO PLOTS
>>>>>>> pcrs-r: implemented rpy2

class RSpecifics(languages.BaseLanguage):
	"""
	Representation of R language (visualizer not supported):
	"""
<<<<<<< HEAD
	def run_test(self, user_script, sol_script):
		"""
		@param str user_script
		@param str sol_script

		Return dictionary <ret> containing results of a test run.
		<ret> has the following mapping:
		'test_val' -> <user_script> output (if successful),
		'sol_val' -> <sol_script> output (if successful),
		'graphics' -> path to graphics (if any),
		'sol_graphics' -> path to solution's graphics (if any),
		'passed_test' -> True if <user_script> outputs <expected_val>,
		'exception' -> exception message (if any)
		"""
		# Just a hash we'll use as a unique name
		f_sha = sha1(str.encode("{}".format(user_script+str(datetime.now())))).hexdigest()
		try:
			ret = self.run(user_script)
			solution = self.run(sol_script)

			if "exception" in solution or "exception" in ret:
				ret["passed_test"] = False
				return ret

			ret["passed_test"] = (ret["test_val"] == solution["test_val"])
			ret["sol_val"] = solution["test_val"]

			if "graphics" in solution.keys():
				ret["sol_graphics"] = solution["graphics"]
		except Exception as e:
			ret["exception"] = str(e)
			ret["passed_test"] = False

		return ret


	def run(self, script):
		"""
		@param str script

		Returns dictionary <ret> containing output of <script>.
		<ret> has the following mapping:
		'test_val' -> <script> output, if successful,
		'graphics' -> path to graphics (if any),
		'exception' -> exception message (if any)
		"""
		# Just a hash we'll use as a unique name
		f_sha = sha1(str.encode("{}".format(script+str(datetime.now())))).hexdigest()
		ret = {}
		try:
			# Path to temporary .txt file for output of script
			path = os.path.join(R_TEMPPATH, f_sha) + ".txt"
			# Path to temporary .png file for graphics of script
			g_path = path[:-4] + ".png"

			exec_r = robjects.r
			# Clear R global environment and redirect stdout to temporary .txt file
			exec_r("rm(list = ls(all.names=TRUE))")
			exec_r("sink(\"{}\")".format(path))

			# Sets the graphical output to a temporary file
			exec_r("png(\"{}\")".format(g_path)) # output to pdf for multiple graphs

			# Remove empty lines from R code
			script = self.strip_empty_lines(script)

			# Execute script
			exec_r(script)

			# Shutdown current device
			exec_r("dev.off()")

			exec_r("sink()") # prevent sink stack from getting full
			# Read and remove temporary .txt
			with open(path, "r") as f:
				ret["test_val"] = f.read()
			os.remove(path)

			# If graphics exist, return the path
			if os.path.isfile(g_path):
				ret["graphics"] = f_sha
			else:
				ret["graphics"] = None
		except Exception as e:
			os.remove(path)
			ret.pop("test_val", None)
			ret["exception"] = str(e)
		return ret


	def strip_empty_lines(self, script):
		"""
		@param str script

		Returns script with all empty lines stripped from it so R code is correct.
		"""
		all_elements = script.split("\n")
		split_elements = [element for element in all_elements if element != ""]

		ret_str = ""
		for i in range(len(split_elements)):
			ret_str += split_elements[i].strip()
			if i != (len(split_elements) - 1):
				ret_str += "\n"

		return ret_str
=======
	def run_test(self, user_script, test_script, args=[], plot=False):
		"""
		@param list args: list of input arguments into wrapper main function
		@param bool plot: True if output includes a plot

		Return dictionary <ret> containing results of a test run.
		<ret> has the following mapping:
		'test_val' -> output of <user_script>,
		'plot' -> path to plot (if any),
		'passed_test' -> True if, given <args>,
			output of <user_script> is equal to output of 
			<test_script> - otherwise False
		'exception' -> exception message, if there are any

		=== Preconditions ===
		Script arguments must be wrapped in a main() function
		with same number of arguments as test_input
		i.e.
		main <- function(...) {
			... BODY HERE ...
		}
		"""
		ret = {}
		try:
			exec_r = robjects.r
			# Clear R global environment
			exec_r("rm(list = ls(all.names=TRUE))")
			user_res = exec_r(user_script)(*args)
			ret['test_val'] = str(user_res)
			if plot:
				f_sha = sha1(str.encode("{}".format(user_script+str(datetime.now())))).hexdigest()
				# View should render the .png file, then delete it.
				exec_r("dev.copy(png, {}\{}.png)".format(R_STATICFILES, f_sha))
				exec_r("dev.off()")
			exec_r("rm(list = ls(all.names=TRUE))")
			test_res = exec_r(test_script)(*args)
			ret['passed_test'] = (ret['test_val'] == str(test_res))
		except Exception as e:
			ret['test_val'] = str(e)
			ret['passed_test'] = False
			ret['exception'] = str(e)
>>>>>>> pcrs-r: implemented rpy2
