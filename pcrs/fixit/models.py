from django.db import models
from users.models import PCRSUser, Section

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.utils import timezone

from problems.pcrs_languages import GenericLanguage
from pcrs.model_helpers import has_changed
from problems.models import (AbstractProgrammingProblem, AbstractSubmission,
        SubmissionPreprocessorMixin, AbstractTestCaseWithDescription,
        AbstractTestRun,
        testcase_delete, problem_delete)
from pcrs.models import AbstractSelfAwareModel
from pcrs.settings import PROJECT_ROOT
import python_ta
import io, re, os, tempfile
from contextlib import redirect_stdout  


# Create your models here:

class StudentFixitProfile(AbstractSelfAwareModel):
    user = models.ForeignKey(PCRSUser, on_delete=models.CASCADE)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE)
    # is_control_group = models.BooleanField("is control group", default=False)
    problem_id = models.IntegerField(default=9999)
    problem_type = models.CharField("problem type", max_length=100, blank=True, null=True)
    submission_time = models.DateTimeField(default=timezone.now)

class ProblemRecommendedFixit(AbstractSelfAwareModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(PCRSUser, on_delete=models.CASCADE)
    problem_type = models.CharField("problem type", max_length=100, blank=True, null=True)
    problem_id = models.IntegerField()

