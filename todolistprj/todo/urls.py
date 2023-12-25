from django.urls import path
from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    CustomLoginView,
    RegisterPage,
    ExportCsvView,
    PasswordChange,
    PasswordChangeDone,
)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TaskList.as_view(), name= "task"),
    path('task-create/', TaskCreate.as_view(), name= "task-create"),
    path('login/', CustomLoginView.as_view(), name= "login"),
    path('logout/', LogoutView.as_view(next_page='login'), name= "logout"),
    path('register/', RegisterPage.as_view(), name= "register"),
    path('task/<int:pk>/', TaskDetail.as_view(), name= "tasks-detail"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name= "tasks-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name= "tasks-delete"),
    path('export-csv/', ExportCsvView.as_view(), name='export-csv'),
    path('password_change/', PasswordChange.as_view(template_name = 'todo/password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(template_name = 'todo/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'todo/registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'todo/registration/password_reset_done.html'),  name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name= 'todo/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'todo/registration/password_reset_complete.html'), name='password_reset_complete'),
]
