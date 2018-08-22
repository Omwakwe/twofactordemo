from django.conf.urls import url
from accounts.views import *
from django.contrib.auth.views import logout
from django.conf import settings

urlpatterns = [
	url(r'^$', Home.as_view(), name='home'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^secret/$', Secret.as_view(), name='secret'),
    url(r'^accountInfo/$', AccountInfo.as_view(), name='accountInfo'),

    url(r'^confirmEmail/(?P<token>\w+)/$', ConfirmEmail.as_view(), name='confirmEmail'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]