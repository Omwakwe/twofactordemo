from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, FormView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.base_user import BaseUserManager

from django_otp.decorators import otp_required
from two_factor.views import OTPRequiredMixin
from two_factor.views.utils import class_view_decorator

from accounts.forms import SignupForm,LoginForm,ProfileForm
from accounts.models import User

def send_user_email(email_link,recipients='starfordomwakwe@gmail.com'):
    subject = 'Account activation email'
    message = ' click on the following link to activate your two factor account '+ email_link
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipients,]
    send_mail( subject, message, email_from, recipient_list )

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ( str(user.pk) + str(timestamp) + str(user.is_active))

class Home(CreateView):
    template_name = "accounts/index.html"

    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        # try:
        #     send_user_email()
        # except Exception as e:
        #     print("Error sending email, check the email settings are correct")
        
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
                login(request, new_user)
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
        if self.request.user.email != '' or self.request.user.email != '':
            return True
        else:
            return False

    def get_login_url(self):
        return '/accountInfo/'

    def dispatch(self, *args, **kwargs):
        return super(Secret, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {}
        context['loginForm'] = LoginForm()
        return render(request, self.template_name, context)

class AccountInfo(LoginRequiredMixin,CreateView):
    template_name = "accounts/profile_update.html"

    def dispatch(self, *args, **kwargs):
        return super(AccountInfo, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        account_activation_token = TokenGenerator()
        user_id = request.user.id
        current_user = User.objects.filter(id = user_id)[0]

        context['profileForm'] = ProfileForm(instance = current_user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(data=request.POST or None)
        response_data ={}

        user_id = request.user.id
        current_user = User.objects.filter(id = user_id)[0]

        user_name = request.POST['user_name']
        old_password = request.POST['old_password']
        # new_password = request.POST['new_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        last_name = request.POST['last_name']

        user = authenticate(request, user_name=user_name, password=old_password)

        if user is not None:
            # user.set_password(new_password)
            user.user_name=user_name
            user.email=email
            user.first_name=first_name
            user.second_name=second_name
            user.last_name=last_name
            user.save()

            response_data['success']     = 'yes'
            response_data['success_msg'] = 'Successfully updated user'
            try:
                if user.email_confirmed == False:
                    urltoken = BaseUserManager().make_random_password(15)
                    user.activation_code = urltoken
                    user.save()

                    email_link = 'http://34.215.13.107/confirmEmail/'+str(urltoken)+"/"
                    send_user_email(email_link,email)
            except Exception as e:
                print("Error sending email, check the email settings are correct")
        else:
            # print('password_confirm !== password')
            response_data['success']     = 'no'
            response_data['success_msg'] = 'password dont match'

        return JsonResponse(response_data)

class ConfirmEmail(LoginRequiredMixin,CreateView):
    template_name = "accounts/email_confirmed.html"

    def dispatch(self, *args, **kwargs):
        return super(ConfirmEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        token = self.kwargs['token']

        print('token',token)      
        
        try:
            user = User.objects.get(activation_code=token)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.email_confirmed = True
            user.save()
            # login(request, user)
            # return redirect('home')
        return render(request, self.template_name, context)