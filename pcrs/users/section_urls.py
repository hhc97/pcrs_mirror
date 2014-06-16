from django.conf.urls import patterns, url
from pcrs.generic_views import GenericCourseStaffDeleteView

from users.section_views import *

urlpatterns = patterns('',
    url(r'^list$', SectionListView.as_view(),name='section_list'),
    url(r'^create$', SectionCreateView.as_view(),name='section_create'),
    url(r'^(?P<pk>[\w-]+)$', SectionUpdateView.as_view(),name='section_update'),
    url(r'^(?P<pk>[\w-]+)/delete$', GenericCourseStaffDeleteView.as_view(model=Section), name='section_delete'),
)