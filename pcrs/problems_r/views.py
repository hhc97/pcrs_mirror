from django.core.urlresolvers import reverse
from django.http import HttpResponse
from problems_r.models import Script
from problems_r.forms import ScriptForm
from pcrs.generic_views import (GenericItemListView, GenericItemCreateView)
from django.views.generic import (DetailView, DeleteView)
from users.views_mixins import CourseStaffViewMixin
from pcrs.settings import PROJECT_ROOT
import os

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

class ScriptDeleteView(ScriptView, DeleteView):
	"""
	Delete an existing R Script.
	"""
	template_name = "problems_r/script_check_delete.html"

def render_graph(request, image):
	"""
	Render R graph image and delete it.
	"""
	targ_script = Script.objects.get(pk=image)
	path = os.path.join(PROJECT_ROOT, "languages/r/CACHE/", targ_script.graphics) + ".png"
	# Check whether the graph already exists and generates it if not
	if not os.path.isfile(path):
		ret = targ_script.generate_graphics()
		path = os.path.join(PROJECT_ROOT, "languages/r/CACHE/", targ_script.graphics) + ".png"

	# Display the graph on the browser then delete
	graph = open(path, "rb").read()
	os.remove(path)
	return HttpResponse(graph, content_type="image/png")
