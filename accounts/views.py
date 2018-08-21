from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, FormView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django_otp.decorators import otp_required
from two_factor.views import OTPRequiredMixin
from two_factor.views.utils import class_view_decorator

from accounts.forms import SignupForm,LoginForm
from accounts.models import User


class Home(CreateView):
    template_name = "accounts/index.html"

    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            print('user is',user.user_name,user.email)
        return render(request, self.template_name, {})

class Signup(CreateView):
    template_name = "accounts/signup.html"

    def dispatch(self, *args, **kwargs):
        return super(Signup, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {}
        context['signupForm'] = SignupForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignupForm(data=request.POST or None)
        response_data ={}

        if form.is_valid():
            user_name = request.POST['user_name']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            email = request.POST['email']

            if password_confirm == password:
                new_user = User(user_name=user_name, email=email)
                new_user.set_password(password)
                new_user.save()

                print('user_id',new_user.id)
                response_data['success']     = 'yes'
                response_data['success_msg'] = 'Successfully signed up'
                # return redirect('/home/')
            else:
                # print('password_confirm !== password')
                response_data['success']     = 'no'
                response_data['success_msg'] = 'password dont match'
        else:
            # print('form is not valid',form.errors)
            response_data['success']     = 'no'
            response_data['success_msg'] = 'form not valid'

        return JsonResponse(response_data)


class Login(CreateView):
    template_name = "accounts/login.html"

    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            print('user is',user.user_name)
        context = {}
        context['loginForm'] = LoginForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST or None)
        response_data ={}

        if form.is_valid():
            user_name = request.POST['user_name']
            password = request.POST['password']
            user = User.objects.get(user_name=user_name)

            checked_user = user.check_password(password)
            print('checked_user is',checked_user)

            if checked_user:
                response_data['success']     = 'yes'
                response_data['success_msg'] = 'Successfully logged in'
            else:
                response_data['success']     = 'no'
                response_data['success_msg'] = 'username and password dont match'
        else:
            print('form is not valid',form.errors)
            response_data['success']     = 'no'
            response_data['success_msg'] = 'form not valid'

        return JsonResponse(response_data)

class Logout(LoginRequiredMixin,CreateView):
    template_name = "accounts/secret.html"

    def dispatch(self, *args, **kwargs):
        return super(Logout, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            print('user is',user.user_name)
        context = {}
        context['loginForm'] = LoginForm()
        return render(request, self.template_name, context)

@class_view_decorator(never_cache)
class Secret(OTPRequiredMixin,UserPassesTestMixin,CreateView):
    template_name = "accounts/secret.html"

    def test_func(self):
        # return self.user.email != '' or self.user.email != ' '
        return True

    # def get_login_url(self):
    #     return '/accountInfo/'

    def dispatch(self, *args, **kwargs):
        return super(Secret, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {}
        context['loginForm'] = LoginForm()
        return render(request, self.template_name, context)

class AccountInfo(CreateView):
    template_name = "accounts/email.html"

    def dispatch(self, *args, **kwargs):
        return super(AccountInfo, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['signupForm'] = SignupForm()
        return render(request, self.template_name, context)