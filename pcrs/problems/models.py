from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max, Q, Count, F
from django.utils import timezone
from django.conf import settings

import content.models
from content.tags import AbstractTaggedObject
from pcrs.models import (AbstractNamedObject, AbstractGenericObjectForeignKey,
                         AbstractSelfAwareModel)
from users.models import PCRSUser, Section, AbstractLimitedVisibilityObject


def get_problem_labels():
    """
    Return the list app_labels of apps that contain a Problem class.
    """
    return [c.app_label for c in ContentType.objects.filter(Q(model='problem'))]


def get_problem_content_types():
    return ContentType.objects.filter(Q(model='problem'))


class AbstractProblem(AbstractSelfAwareModel, AbstractLimitedVisibilityObject,
                      AbstractTaggedObject):
    """
    A base class for all problems.

    All problems have visibility level, and optionally tags, and are self-aware.
    """
    challenge = models.ForeignKey(content.models.Challenge, null=True, blank=True,
        related_name='%(app_label)s_%(class)s_related', on_delete=models.SET_NULL)

    max_score = models.SmallIntegerField(default=0, blank=True)

    # bug in 1.5 does not allow this generic relation
    # TODO: this should work when we upgrade to >1.6
    # content_problem = generic.GenericRelation(
    #     content.models.ContentSequenceItem, content_type_field='content_type',
    #     object_id_field='object_id',
    #     related_name='%(app_label)s_%(class)s_content_problem')

    class Meta:
        abstract = True

    def __str__(self):
        description = self.description[:150]
        if len(self.description) > 150:
            description += '...'
        return description

    @classmethod
    def get_problem_type_name(cls):
        return cls.__module__.split('.')[0].replace('problems_', '')

    @classmethod
    def get_module_name(cls):
        return cls.__module__.split('.')[0]

    @classmethod
    def get_challenge_to_problem_number(cls):
        """
        Return a dictionary mapping Challenge pk to the the total number of
        problems of this type in that Challenge.
        """
        problems = cls.objects.values('challenge_id')\
                              .annotate(number=Count('id'))\
                              .order_by()
        return {d['challenge_id']: d['number']for d in problems}

    @classmethod
    def get_base_url(cls):
        """
        Return the url prefix for the problem type.
        """
        return '{site}/problems/{typename}'\
            .format(site=settings.SITE_PREFIX,
                    typename=cls.get_problem_type_name())

    def get_absolute_url(self):
        return '{base}/{pk}'.format(base=self.get_base_url(), pk=self.pk)

    def best_per_user_before_time(self, deadline=timezone.now()):
        """
        Return a list of dictionaries of the form {user_id: , score:)
        representing the best submissions for every user who submitted a
        solution to this problem BEFORE deadline.

        Used for generating CSV reports and problem analysis.
        """
        return self.submission_set.filter(timestamp__lt=deadline)\
            .values('user_id').annotate(score=Max('score')).order_by()

    def clear_submissions(self):
        """
        Delete all submissions to this problem.
        """
        self.submission_set.all().delete()

    def get_best_submission_per_student_after_time(self, section, time):
        """
        Return the list of best submissions made after time in the section.
        """
        return self.submission_set.all().filter(section=section,
                                                timestamp__gt=time,
                                                has_best_score=True)

    def get_monitoring_data(self, section, time):
        """
        Return data for real-time monitoring.
        """
        correct, incorrect = 0, 0
        s_ids = set()
        max_score = self.max_score

        for submission in self.get_best_submission_per_student_after_time(
                section, time):
            s_ids.add(submission.pk)
            if submission.score == max_score:
                correct += 1
            else:
                incorrect += 1

        data = self.get_testitem_data_for_submissions(s_ids)
        return {
            'submissions': [correct, incorrect],
            # order by the id of related object
            'data': [data[key] for key in sorted(data.keys())]
        }


class AbstractProgrammingProblem(AbstractProblem):
    """
    Base class for programming problems.

    Programming problems may have starter starter code and solution.
    """

    starter_code = models.TextField(blank=True)
    solution = models.TextField(blank=True)

    class Meta:
        abstract = True

    def get_testitem_data_for_submissions(self, s_ids):
        """
        Return a list of tuples summarizing for each testcase how many times it
        passed and failed in submissions with pk in s_ids.
        Each tuple has the form (testcase_id, times_passed, times_failed).
        """
        data = self.get_testrun_class().objects.filter(submission_id__in=s_ids)\
            .values('testcase_id', 'test_passed')\
            .annotate(count=Count('test_passed'))
        results = {}
        # data is a list of dictionaries
        # {test_case_id: '',  test_passed: ', count: ''}
        # every dictionary encodes how many times a testcase passed or failed
        for dict in data:
            opt_id = dict['testcase_id']
            count = dict['count']
            res = results.get(opt_id, [0, 0])
            if dict['test_passed'] is True:
                res[0] = count
            if dict['test_passed'] is False:
                res[1] = count
            results[opt_id] = res
        return results


class AbstractNamedProblem(AbstractNamedObject, AbstractProgrammingProblem):
    """
    A problem extended to have a required name and description.
    """
    class Meta:
        abstract = True


class AbstractSubmission(AbstractSelfAwareModel):
    """
    Base submission class.

    Submission is associated with a user and a problem, and optionally
    a section, and has a score, usually out of the total number of testcases
    that the associated problem has.
    """
    user = models.ForeignKey(PCRSUser, to_field='username',
                                on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_related')
    section = models.ForeignKey(Section, blank=True,  null=True,
                                on_delete=models.SET_NULL,
                                related_name='%(app_label)s_%(class)s_related')
    timestamp = models.DateTimeField(default=timezone.now)
    submission = models.TextField(blank=True, null=True)
    score = models.SmallIntegerField(default=0)
    has_best_score = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-timestamp']

    def __str__(self):
        return '{problem} by {user} on {time}'.format(
            problem=self.problem, user=self.user.username,
            time=self.timestamp)

    def set_best_submission(self):
        """
        Update the submission such that the latest submission with highest score
        is marked with has_best_score.
        """
        try:
            current_best = self.__class__.objects.get(
                user=self.user, problem=self.problem, has_best_score=True)
            if self.score >= current_best.score and self.pk != current_best.pk:
                current_best.has_best_score = False
                current_best.save()
                self.has_best_score = True
        except self.__class__.DoesNotExist:
            self.has_best_score = True
        finally:
            self.save()

    def set_score(self):
        """
        Set the score of this submission to the number of testcases that
        the submission passed.
        Create a record of the user completing the problem if the score on
        the submission is the highest score possible on the problem.
        """
        self.score = self.testrun_set.filter(test_passed=True).count()
        self.save()
        self.set_best_submission()

    @classmethod
    def get_best_before_deadline(cls, user):
        """
        Return a dictionary mapping challenge_pk to the number of problems
        the user has completed in each Challenge.
        """
        subs = cls.objects\
            .filter(user=user, score=F('problem__max_score'),
                    problem__challenge__quest__sectionquest__section=user.section,
                    timestamp__lt=F('problem__challenge__quest__sectionquest__due_on'))\
            .values('problem__challenge')\
            .annotate(solved=Count('problem', distinct=True))\
            .order_by()
        return {d['problem__challenge']: d['solved']for d in subs}

    @classmethod
    def get_best_attempts_before_deadlines(cls, user):
        """
        Return a dictionary mapping problem pk to the user's best score on the
        problem with that pk, before the challenge deadline.
        """
        subs = cls.objects\
            .filter(user=user,
                    problem__challenge__quest__sectionquest__section=user.section,
                    timestamp__lt=F('problem__challenge__quest__sectionquest__due_on'))\
            .values('problem_id').annotate(best=Max('score')).order_by()
        return {d['problem_id']: d['best']for d in subs}

    @classmethod
    def grade(cls, quest, section):
        return cls.objects\
            .filter(problem__challenge__quest=quest, user__section=section,
                    problem__challenge__quest__sectionquest__section=section,
                    timestamp__lt=F('problem__challenge__quest__sectionquest__due_on'))\
            .values('user', 'problem').annotate(best=Max('score')).order_by()


class AbstractTestCase(AbstractSelfAwareModel):
    """
    Base testcase class.

    TestCase is associated with a single problem.
    Each problem type should implement its own TestCase according to the
    problem semantics, as well as define what it means for a testcase to pass.
    """

    class Meta:
        abstract = True
        ordering = ['pk']

    def __str__(self):
        return '{problem}: testcase {pk}'.format(
            pk=self.pk, problem=self.problem)

    def get_absolute_url(self):
        return '{problem}/testcase/{pk}'.format(
            problem=self.problem.get_absolute_url(), pk=self.pk)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            self.problem.max_score += 1
            self.problem.save()
        super().save(force_insert, force_update, using, update_fields)


class AbstractTestRun(models.Model):
    """
    Base testrun class.

    A testrun is associated with a single submission, and a single TestCase,
    and records whether that testcase for that submission has passed.
    """
    test_passed = models.BooleanField()

    class Meta:
        abstract = True

    def __str__(self):
        return '{submission}: testcase {pk}'.format(
            submission=self.submission, pk=self.testcase.pk)

    def get_history(self):
        return {
            'visible': self.testcase.is_visible,
            'input': self.testcase.test_input,
            'output': self.testcase.expected_output,
            'passed': self.test_passed,
            'description': self.testcase.description
        }

# Signal handlers

def testcase_delete(sender, instance, **kwargs):
    """
    Updates the submission scores to a problem when its testcase is deleted.
    """
    try:
        problem = instance.problem
        problem.max_score -= 1
        problem.save()

        submissions_affected = problem.submission_set.all()
        for submission in submissions_affected:
            submission.set_score()
    except sender.get_problem_class().DoesNotExist:
        # problem no longer exists, submissions will be deleted automatically
        # so no need to update scores
        pass
