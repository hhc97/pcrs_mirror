from django.conf.urls import include, url

from .views import *

from . import views
from problems.views import *
from problems_multiple_choice.forms import ProblemForm
from problems_multiple_choice.models import *
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt


router = routers.DefaultRouter()
router.register(r'StudentFixitProfile', StudentFixitProfileViewSet)

urlpatterns = [
    url(r'^main/', studentFixitView.as_view()),
    url(r'^api/', include(router.urls))
]
