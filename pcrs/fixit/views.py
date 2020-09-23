from collections import *
from django.shortcuts import render
from fixit.models import *
from django.views.generic import TemplateView
from problems_multiple_choice.models import *
from problems_multiple_choice.models import Problem   
from problems_multiple_choice.forms import SubmissionForm as MCSubmissionForm
from problems_multiple_choice.views import *
from problems_python.models import Problem as PythonProblem
from problems.forms import ProgrammingSubmissionForm 
from fixit.serializers import *
import problems_multiple_choice.models
import problems_python.models
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

class studentFixitView(TemplateView):
    template_name = 'fixit/student_fixit_view.html'
    model = ProblemRecommendedFixit
    form_class = MCSubmissionForm 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_date = ProblemRecommendedFixit.objects.filter(user=self.request.user).order_by('-date').first().date 
        context['recommended_problems'] = ProblemRecommendedFixit.objects.filter(user=self.request.user).filter(date=latest_date)
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
            if isinstance(problem, Problem):
                forms[problem.get_problem_type_name()][problem.pk] = MCSubmissionForm(problem=problem, simpleui=self.request.user.use_simpleui)
            if isinstance(problem, PythonProblem):
                forms[problem.get_problem_type_name()][problem.pk] = ProgrammingSubmissionForm(problem=problem, simpleui=self.request.user.use_simpleui)
        context['forms'] = forms
        


        return context

class StudentFixitProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentFixitProfile.objects.all()
    serializer_class = StudentFixitProfileSerializer
