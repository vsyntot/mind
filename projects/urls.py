from django.conf.urls import url
from django.urls import path, re_path
from projects.views import *

app_name = "projects"
urlpatterns = [
    path('create', ProjectCreateView.as_view()),
    path('', ProjectListView.as_view()),
    path('<int:pk>', ProjectDetailView.as_view()),
    path('checkdeploy', ProjectDetailView.as_view()),
    url(r'^download/(?P<path>.*)$', download),
]
