from django.conf.urls import url

from pythonizame.apps.jobboard.views import (JobbordListView, JobDetailView, JobAddView)
from pythonizame.apps.jobboard.views import (JobbordMyJobsListView, JobEditView, JobDeleteView, JobChangeToReviewView)


app_name = "jobboard"

urlpatterns = [
    url(r'^job/list/', JobbordListView.as_view(), name='list'),
    url(r'^job/my-list/', JobbordMyJobsListView.as_view(), name='my-list'),
    url(r'^job/add/', JobAddView.as_view(), name='add'),
    url(r'^job/edit/(?P<job_id>[0-9]+)/', JobEditView.as_view(), name='edit'),
    url(r'^job/detail/(?P<pk>[0-9]+)/', JobDetailView.as_view(), name='detail'),
    url(r'^job/delete/(?P<job_id>[0-9]+)/', JobDeleteView.as_view(), name='delete'),
    url(r'^job/change-to-review/(?P<job_id>[0-9]+)/', JobChangeToReviewView.as_view(), name='change-to-review')
]
