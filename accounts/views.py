from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, FormView


class Home(CreateView):
    template_name = "accounts/index.html"

    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})