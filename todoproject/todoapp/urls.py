from django.urls import path
from .views import UserRegistrationView, TaskAssignView, Loginview, TaskCheckView, TaskCheckApiView

urlpatterns=[
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',Loginview.as_view(),name='login'),
    path('taskpost/',TaskAssignView.as_view()),
    path('taskpost/<int:id>/',TaskAssignView.as_view()),
    path('taskcheck/<int:id>/',TaskCheckView.as_view()),
    path('taskcheckview/<int:id>/',TaskCheckApiView.as_view())
]
