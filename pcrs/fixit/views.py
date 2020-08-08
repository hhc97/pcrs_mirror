from collections import *
from django.shortcuts import render
from fixit.models import *
from django.views.generic import TemplateView
from problems_multiple_choice.models import *
from problems_multiple_choice.forms import SubmissionForm as MCSubmissionForm
from problems_multiple_choice.views import *
from problems_python.models import Problem as PythonProblem
from problems.forms import ProgrammingSubmissionForm 

class studentFixitView(TemplateView):
    template_name = 'fixit/student_fixit_view.html'
    model = problemRecommendedFixit
    form_class = MCSubmissionForm 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_problems'] = problemRecommendedFixit.objects.filter(user=self.request.user)
        context['recommended_problems_content'] = []
        for problem in context['recommended_problems']:
            if problem.problem_type == 'multiple_choice':
                filter_problems = Problem.objects.get(id=problem.problem_id)
                context['recommended_problems_content'].append(filter_problems)     
            elif problem.problem_type == 'python':
                filter_problems = PythonProblem.objects.get(id=problem.problem_id)
                context['recommended_problems_content'].append(filter_problems)

        forms = defaultdict(dict)
        for problem in context['recommended_problems_content']:
            if problem.problem_type == "multiple_choice":
                forms[problem.problem_type][problem.pk] = MCSubmissionForm(problem=problem, simpleui=self.request.user.use_simpleui)
            elif problem.problem_type == "python":
                forms[problem.problem_type][problem.pk] = ProgrammingSubmissionForm(problem=problem, simpleui=self.request.user.use_simpleui)
        context['forms'] = forms
        


        return context


