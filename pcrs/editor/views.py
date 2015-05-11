import json
import datetime
import logging

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import (DetailView, UpdateView, DeleteView, FormView, View)
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import localtime
from problems.forms import ProgrammingSubmissionForm
from pcrs.generic_views import (GenericItemCreateView, GenericItemListView,
                                GenericItemUpdateView)
from users.views import UserViewMixin
from users.views_mixins import ProtectedViewMixin
import problems_c.models as c_models
import problems_python.models as python_models

class EditorViewMixin:
    def get_section(self):
        return None

    def get_problem(self):
        """
        Return the Problem object for the submission.
        """
        logging.info('page_processor logging test')
        if(self.pType == 'c'):
        	p = c_models.Problem(name="blank", starter_code="")
        elif(self.pType == 'python'):
       		p = python_models.Problem(name="blank", starter_code="")
       	else:
       		logging.info('NONE PTYPE')
       		p = None
        return p

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['problem'] = self.get_problem()
        return kwargs

    def get_context_data(self, **kwargs):
        return None

    def record_submission(self, request):
        """
        Record the submission and return the results of running the testcases.
        """
        submission_model = self.model.get_submission_class()
        submission_code = request.POST.get('submission', '')
        results, error = [], None
        if submission_code:
            submission = submission_model.objects.create(
                user=request.user, problem=self.get_problem(),
                section=self.get_section(), submission=submission_code)
            results, error = submission.run_testcases(request)
            submission.set_score()
            self.object = submission
        return results, error

    def post(self, request, *args, **kwargs):
        """
        Record the submission and redisplay the problem submission page,
        with latest submission prefilled.
        """
        form = self.get_form(self.get_form_class())
        results, error = self.record_submission(request)
        return self.render_to_response(
            self.get_context_data(form=form, results=results, error=error,
                                  submission=self.object))


class EditorView(ProtectedViewMixin, EditorViewMixin, SingleObjectMixin,
                     FormView, UserViewMixin):
    """
    Create a submission for a problem.
    """
    pType = None
    form_class = ProgrammingSubmissionForm
    object = None