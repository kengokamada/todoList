from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django .views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task

import csv
from django.views import View

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
import requests

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user = self.request.user)
        context['count'] = context['task'].filter(complete = False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains = search_input)
            context['search-input'] = search_input
#天気予報API
        try:
            url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=95ac8b70b99b1f7b0165f402e641a49e'
            city = '埼玉県'

            r = requests.get(url.format(city)).json()
            city_weather = {
                'city' : city,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
            context['city_weather'] = city_weather
        # return context
        except requests.RequestException as e:
            context['city_weather'] = {'error' : 'Failed to fetch weather data '}
        return context

#パスワードリセット
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'todo/registration/password_reset_subject.txt'
    email_template_name = 'todo/registration/password_reset_email.html'
    template_name = 'todo/registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'todo/registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'todo/registration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'todo/registration/password_reset_complete.html'

#パスワード変更
class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'password_change_done.html'

#CSVエクスポート
class ExportCsvView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="task.csv"'

        writer = csv.writer(response)
        writer.writerow(['\ufeffUser', 'Title', 'Description', 'Created'])

        user_tasks = Task.objects.filter(user = self.request.user)

        for task in user_tasks:
            writer.writerow([task.user, task.title, task.description, task.created])
        return response

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, **kwargs)
