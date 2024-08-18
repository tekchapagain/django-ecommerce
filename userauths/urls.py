from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [

	# User Auths
	path("sign-up/", views.register_view, name="sign-up"),
	path("sign-in/", views.login_view, name="sign-in"),
	path("sign-out/", views.logout_view, name="sign-out"),

	# User Account
	path("account/", views.account, name="account"),
]