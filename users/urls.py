from django.urls import re_path, include, path

from .views import RegistrationAPIView
from .views import LoginAPIView, UsersListView, UsersDetailView

urlpatterns = [
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    path(r'', UsersListView.as_view(), name='users_list'),
    path(r'<int:pk>', UsersDetailView.as_view(), name='users_update'),
]