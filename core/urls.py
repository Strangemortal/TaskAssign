from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
   
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-task/', views.create_task, name='create_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/<int:task_id>/comment/', views.add_comment, name='add_comment'),
    path('tasks/<int:task_id>/submit/', views.submit_for_review, name='submit_for_review'),
    path('tasks/submitted/', views.submitted_tasks, name='submitted_tasks'),
    # path('verify-task/<int:task_id>/', views.verif, name='verify_task'), 
    path('tasks/review/<int:task_id>/', views.review_task, name='review_task'),
    path('signup/', views.signup_view, name='signup'),

    path("pending-users/", views.pending_users, name="pending_users"),
path("approve-user/<int:user_id>/", views.approve_user, name="approve_user"),
path("reject-user/<int:user_id>/", views.reject_user, name="reject_user"),


]
