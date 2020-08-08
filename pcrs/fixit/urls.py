from django.conf.urls import url 

from .views import *

from problems.views import *
from problems_multiple_choice.forms import ProblemForm
from problems_multiple_choice.models import *

urlpatterns = [
    url(r'^main/', studentFixitView.as_view()),
]
