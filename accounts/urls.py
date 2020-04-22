from django.urls import path, include

from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('resetPassword/', views.change_password, name='change_password'),
	#path('login/', views.login, name='login'),
]
