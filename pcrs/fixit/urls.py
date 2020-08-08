from django.conf.urls import url 

from fixit.views import *

from problems.views import *
from problems_multiple_choice.forms import ProblemForm
from problems_multiple_choice.models import *

urlpatterns = [
    url(r'^main/', studentFixitView.as_view()),
]
