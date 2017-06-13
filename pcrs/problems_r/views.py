from django.core.urlresolvers import reverse
from django.http import HttpResponse
from problems_r.models import Script, delete_graph, FileSubmissionManager, Problem
from problems_r.forms import ScriptForm, FileSubmissionForm
from pcrs.generic_views import (GenericItemListView, GenericItemCreateView)
from django.views.generic import (DetailView, DeleteView, View)
from users.views_mixins import CourseStaffViewMixin
from pcrs.settings import PROJECT_ROOT, DEBUG
from users.models import PCRSUser
from problems.views import SubmissionView, FileUploadMixin, SubmissionAsyncView, DateEncoder
from problems.models import FileUpload
from django.core.exceptions import ObjectDoesNotExist
import os

# MIGHT DELETE THIS
import logging
from django.utils.timezone import localtime, now
import json

class ScriptView(CourseStaffViewMixin):
	"""
	Base R Script view
	"""
	model = Script

	def get_success_url(self):
		return reverse("script_list")

class ScriptListView(ScriptView, GenericItemListView):
	"""
	List R Scripts
	"""
	template_name = "pcrs/item_list.html"

class ScriptCreateView(ScriptView, GenericItemCreateView):
	"""
	Create new R Script.
	"""
	form_class = ScriptForm
	template_name = "problems_r/script_form.html"

class ScriptCreateAndRunView(ScriptCreateView):
	"""
	Create new R Script and run.
	"""
	def get_success_url(self):
		return self.object.get_absolute_url()

class ScriptDetailView(ScriptView, DetailView):
	"""
	View an existing R Script.
	"""
	template_name = "problems_r/script_detail.html"

	def get_context_data(self, **kwargs):
		context = super(ScriptView, self).get_context_data(**kwargs)
		# Check whether the temporary graph image still exists, if not generate it
		if self.object.graphics:
			path = os.path.join(PROJECT_ROOT, "languages/r/CACHE/", self.object.graphics) + ".png"
			if not os.path.isfile(path):
				ret = self.object.generate_graphics()
		return context

class ScriptDeleteView(ScriptView, DeleteView):
	"""
	Delete an existing R Script.
	"""
	template_name = "problems_r/script_check_delete.html"

def render_graph(request, image):
	"""
	Render R graph image and delete it.
	"""
	path = os.path.join(PROJECT_ROOT, "languages/r/CACHE/", image) + ".png"
	# Display the graph on the browser then delete
	graph = open(path, "rb").read()
	delete_graph(image)
	return HttpResponse(graph, content_type="image/png")

class FileSubmissionView(FileUploadMixin, SubmissionView):
	"""
	Adds file submission functionality.
	"""
	form_class = FileSubmissionForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class FileSubmissionAsyncView(FileUploadMixin, SubmissionAsyncView):
	def post(self, request, *args, **kwargs):
		try:
			results = self.record_submission(request)
		except AttributeError: # Probably an anonymous user
			if DEBUG:
				raise
			return HttpResponse(json.dumps({
					'results': ([], "Your session has expired. Please copy your submission (to save it) and refresh the page before submitting again."),
					'score': 0,
					'sub_pk': 0,
					'best': False,
					'past_dead_line': False,
					'max_score': 1}, cls=DateEncoder),
					content_type='application/json')

		problem = self.get_problem()
		user, section = self.request.user, self.get_section()

		logger = logging.getLogger('activity.logging')
		logger.info(str(localtime(self.object.timestamp)) + " | " +
					str(user) + " | Submit " +
					str(problem.get_problem_type_name()) + " " +
					str(problem.pk))
		try:
			deadline = problem.challenge.quest.sectionquest_set\
				.get(section=section).due_on
		except Exception:
			deadline = False
		return HttpResponse(json.dumps({
			'results': results,
			'score': self.object.score,
			'sub_pk': self.object.pk,
			'best': self.object.has_best_score,
			'past_dead_line': deadline and self.object.timestamp > deadline,
			'max_score': self.object.problem.max_score}, cls=DateEncoder),
		content_type='application/json')

class FileManagerView(View):
	"""
	Keeps track of unique problem-user combinations for files.
	"""
	def post(self, request, *args, **kwargs):
		# Retrieve user and problem model instances for combination
		targ_user = PCRSUser.objects.get(username=request.user)
		targ_problem = Problem.objects.get(pk=kwargs['problem'])
		try:
			existing_file = FileSubmissionManager.objects.get(user=targ_user, problem=targ_problem)
			existing_file.file_upload.data = request.body
			existing_file.file_upload.save()
			return HttpResponse(existing_file.file_upload.pk)
		except ObjectDoesNotExist:
			# Create the new FileUpload instance and new FileSubmissionManager for this combo
			new_file = FileUpload(data=request.body)
			new_file.save()
			new_entry = FileSubmissionManager(user=targ_user, problem=targ_problem, file_upload=new_file)
			new_entry.save()
			return HttpResponse(new_file.pk)
