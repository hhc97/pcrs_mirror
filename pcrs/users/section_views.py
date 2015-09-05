from collections import defaultdict
import csv
import time

from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.utils.html import strip_tags
from django.contrib.contenttypes.models import ContentType

from content.models import ContentSequenceItem
from pcrs.generic_views import (GenericItemListView, GenericItemCreateView,
                                GenericItemUpdateView)
from problems.models import (get_problem_content_types,
                             get_submission_content_types)
from users.forms import SectionForm, QuestGradeForm, SectionSelectionForm
from users.models import Section, PCRSUser, MASTER_SECTION_ID
from users.views_mixins import CourseStaffViewMixin


class SectionViewMixin:
    def get_section(self):
        return (self.request.session.get('section', None) or
                self.request.user.section)


class ChangeSectionView(CourseStaffViewMixin, SectionViewMixin, FormView):
    template_name = 'pcrs/crispy_form.html'
    form_class = SectionSelectionForm

    def form_valid(self, form):
        self.request.session['section'] = form.cleaned_data['section']
        return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['section'] = self.get_section()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'View pages as section'
        return context


class SectionListView(CourseStaffViewMixin, GenericItemListView):
    model = Section
    template_name = 'pcrs/section_list.html'

    def get_queryset(self):
        return Section.objects.exclude(section_id=MASTER_SECTION_ID)


class SectionCreateView(CourseStaffViewMixin, GenericItemCreateView):
    model = Section
    form_class = SectionForm

    def get_success_url(self):
        return self.object.get_manage_section_quests_url()


class SectionUpdateView(CourseStaffViewMixin, GenericItemUpdateView):
    model = Section
    form_class = SectionForm


class SectionReportsView(CourseStaffViewMixin, SingleObjectMixin, FormView):
    model = Section
    form_class = QuestGradeForm
    template_name = 'pcrs/crispy_form.html'
    object = None

    def get_initial(self):
        initial = super().get_initial()
        initial['section'] = self.get_object()
        return initial


    def form_valid(self, form):
        section = form.cleaned_data['section']
        quest = form.cleaned_data['quest']
        active_only = bool(form.cleaned_data['active'])
        for_credit = form.cleaned_data['for_credit']

        # return a csv file
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename={0}-{1}-{2}.csv'.\
                format(str(section).replace(" @ ", "_"), quest.name.replace(" ", "_"), time.strftime("%m%d%y"))
        writer = csv.writer(response)

        # query database for this section's problems
        problem_types = get_problem_content_types()
        section_problems = []
        problem_ids = []
        for ctype in problem_types:
            for problem in ctype.model_class().objects\
                    .select_related('challenge')\
                    .filter(challenge__quest=quest, visibility='open')\
                    .order_by('id'):
                section_problems.append(problem)
                problem_ids.append(problem.pk)

        #query database for order of problems and sort problems accordingly
        sorted_section_problems = []
        content_sequence_items = ContentSequenceItem.objects.filter(object_id__in=problem_ids)\
                                 .order_by('content_page__id', 'order')
        for item in content_sequence_items:
            try:
                sorted_section_problems.append([problem for problem in section_problems if problem.pk == item.object_id][0])
            except Exception as e:
                print(e)
                trace = str(e)


        # collect the problem ids, names, and max_scores, and for_credit
        problems, names, max_scores, for_credit_row = [], [], [], []
        for problem in sorted_section_problems:
                # include for_credit and/or not for_credit problems
                is_graded = problem.challenge.is_graded
                if ('fc' in for_credit and is_graded) or ('nfc' in for_credit and not is_graded):
                    problems.append((ctype.app_label, problem.pk))
                    names.append(strip_tags(str(problem)).replace('\n', ' ').replace('\r', ' ') + ' / ' + str(problem.pk))
                    max_scores.append(problem.max_score)
                    for_credit_row.append(is_graded)
        writer.writerow(['problems/ID'] + names)
        writer.writerow(['users/max_scores'] + max_scores)
        writer.writerow(['for credit'] + for_credit_row)

        # collect grades for each student
        results = defaultdict(dict)
        for ctype in get_submission_content_types():
            grades = ctype.model_class().grade(quest=quest, section=section,
                                               active_only=active_only)
            for record in grades:
                problem = (ctype.app_label,
                           record['problem'])
                results[record['user']][problem] = record['best']

        for student_id, score_dict in results.items():
            writer.writerow(([student_id] +
                            [score_dict.get(problem, '') for problem in problems]))

        # collect students in the section who has not submitted anything

        for student in PCRSUser.objects.get_students(active_only=active_only)\
                                       .filter(section=section)\
                                       .exclude(username__in=results.keys()):
            writer.writerow([student.username] + ['' for problem in problems])
        return response
