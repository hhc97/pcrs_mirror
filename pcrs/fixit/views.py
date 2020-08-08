from collections import *
from django.shortcuts import render
from fixit.models import *
from django.views.generic import TemplateView
from problems_multiple_choice.models import *
from problems_multiple_choice.forms import SubmissionForm as MCSubmissionForm
from problems_multiple_choice.views import *


class studentFixitView(TemplateView):
    template_name = 'fixit/student_fixit_view.html'
    model = problemRecommendedFixit
    form_class = MCSubmissionForm 
    
    def get_queryset(self):
        self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_problems'] = problemRecommendedFixit.objects.filter(user=self.request.user)
        context['recommended_problems_content'] = []
        for problem in context['recommended_problems']:
            filter_problems = Problem.objects.get(id=problem.problem_id)
            context['recommended_problems_content'].append(filter_problems)     
        
        forms = defaultdict(dict)
        for problem in context['recommended_problems_content']:
            forms[problem.pk] = MCSubmissionForm(problem=problem, simpleui=self.request.user.use_simpleui)
        context['forms'] = forms
        
        return context


