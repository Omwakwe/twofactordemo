from django.conf.urls import url
from accounts.views import *

urlpatterns = [
    url(r'^home/$', Home.as_view(), name='home'),
]